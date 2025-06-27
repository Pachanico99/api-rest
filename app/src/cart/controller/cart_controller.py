from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.src.cart.service.cart_service import CartService
from app.src.cart.dto.cart_dto import Cart, CartCreate, CartItemCreate, PaymentResponse

router = APIRouter(prefix="/carts", tags=["Carts"])

@router.post("/", response_model=Cart, status_code=status.HTTP_201_CREATED)
async def create_cart(cart_create: CartCreate, db: Session = Depends(get_db)):
    service = CartService(db)
    cart_data = await service.create_cart(cart_create.user_id)
    cart_data["items"] = [] 
    return cart_data

@router.get("/{cart_id}", response_model=Cart)
async def get_cart(cart_id: int, db: Session = Depends(get_db)):
    service = CartService(db)
    return await service.get_cart_details(cart_id)

@router.put("/{cart_id}/items", response_model=Cart)
async def add_item_to_cart(cart_id: int, item: CartItemCreate, db: Session = Depends(get_db)):
    service = CartService(db)
    await service.add_item_to_cart(cart_id, item)
    return await service.get_cart_details(cart_id)

@router.delete("/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    service = CartService(db)
    await service.delete_cart(cart_id)
    return None

@router.post("/{cart_id}/pay", response_model=PaymentResponse)
async def pay_cart(cart_id: int, db: Session = Depends(get_db)):
    service = CartService(db)
    tracking_id = await service.pay_cart(cart_id)
    return {"tracking_id": tracking_id}