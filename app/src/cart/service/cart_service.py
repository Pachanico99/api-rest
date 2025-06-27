import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.src.product.repository.product_repository import ProductRepository
from app.src.cart.dto.cart_dto import CartItemCreate

CARTS: Dict[int, Dict[str, Any]] = {}
USER_CART_MAP: Dict[int, int] = {}
CARTS_LOCK = asyncio.Lock()

MAX_ITEMS_PER_CART = 15
MAX_OPERATIONS_PER_CART = 20
MAX_QUANTITY_PER_PRODUCT = 10
CART_INACTIVITY_MINUTES = 2

class CartService:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)

    async def _get_cart_or_fail(self, cart_id: int) -> Dict[str, Any]:
        async with CARTS_LOCK:
            if cart_id not in CARTS:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cart with id {cart_id} not found.")
            return CARTS[cart_id]

    async def _increment_operations(self, cart_id: int):
        cart = await self._get_cart_or_fail(cart_id)
        cart["operations_count"] += 1
        cart["last_modified"] = datetime.utcnow()
        if cart["operations_count"] > MAX_OPERATIONS_PER_CART:
            await self._delete_cart_from_state(cart_id, cart["user_id"])
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Cart deleted due to exceeding operation limit ({MAX_OPERATIONS_PER_CART}).")

    async def create_cart(self, user_id: int) -> Dict[str, Any]:
        async with CARTS_LOCK:
            if user_id in USER_CART_MAP:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {user_id} already has an active cart.")
            
            cart_id = uuid.uuid4().int & (1<<32)-1
            new_cart = {
                "cart_id": cart_id,
                "user_id": user_id,
                "items": {},
                "operations_count": 0,
                "last_modified": datetime.utcnow()
            }
            CARTS[cart_id] = new_cart
            USER_CART_MAP[user_id] = cart_id
            return new_cart

    async def add_item_to_cart(self, cart_id: int, item_create: CartItemCreate) -> Dict[str, Any]:
        cart = await self._get_cart_or_fail(cart_id)
        await self._increment_operations(cart_id)

        product = self.product_repository.find_by_id(item_create.product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {item_create.product_id} not found.")
        
        current_quantity = cart["items"].get(item_create.product_id, 0)
        new_quantity = current_quantity + item_create.quantity

        if new_quantity > MAX_QUANTITY_PER_PRODUCT:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Cannot have more than {MAX_QUANTITY_PER_PRODUCT} units of the same product.")
        
        if new_quantity > product.get_stock():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Not enough stock for product {product.id}. Available: {product.get_stock()}, Required: {new_quantity}.")

        if item_create.product_id not in cart["items"] and len(cart["items"]) >= MAX_ITEMS_PER_CART:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Cart cannot have more than {MAX_ITEMS_PER_CART} unique items.")
        
        cart["items"][item_create.product_id] = new_quantity
        return cart

    async def get_cart_details(self, cart_id: int) -> Dict[str, Any]:
        cart = await self._get_cart_or_fail(cart_id)
        cart_data = cart.copy()
        cart_data["items"] = [{"product_id": k, "quantity": v} for k, v in cart["items"].items()]
        return cart_data

    async def _delete_cart_from_state(self, cart_id: int, user_id: int):
        if cart_id in CARTS:
            del CARTS[cart_id]
        if user_id in USER_CART_MAP:
            del USER_CART_MAP[user_id]
            
    async def delete_cart(self, cart_id: int):
        cart = await self._get_cart_or_fail(cart_id)
        async with CARTS_LOCK:
            await self._delete_cart_from_state(cart_id, cart["user_id"])

    async def pay_cart(self, cart_id: int) -> int:
        cart = await self._get_cart_or_fail(cart_id)
        user_id = cart["user_id"]

        if not cart["items"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot pay for an empty cart.")
        
        try:
            for product_id, quantity in cart["items"].items():
                product = self.product_repository.find_by_id(product_id)
                if not product or product.get_stock() < quantity:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Stock for product {product_id} changed. Payment failed.")
                
                product.set_stock(product.get_stock() - quantity)
                self.product_repository.save(product)
        except Exception as e:
            raise e

        async with CARTS_LOCK:
            await self._delete_cart_from_state(cart_id, user_id)

        return uuid.uuid4().int & (1<<32)-1


async def cleanup_inactive_carts_task():
    while True:
        await asyncio.sleep(60)
        now = datetime.utcnow()
        inactive_carts_to_delete = []
        
        async with CARTS_LOCK:
            for cart_id, cart_data in CARTS.items():
                if now - cart_data["last_modified"] > timedelta(minutes=CART_INACTIVITY_MINUTES):
                    inactive_carts_to_delete.append((cart_id, cart_data["user_id"]))
            
            for cart_id, user_id in inactive_carts_to_delete:
                print(f"INFO: Deleting inactive cart {cart_id} for user {user_id}")
                if cart_id in CARTS: del CARTS[cart_id]
                if user_id in USER_CART_MAP: del USER_CART_MAP[user_id]
