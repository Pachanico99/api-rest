from sqlalchemy.orm import Session
from typing import Optional, List
import uuid

from app.src.cart.model.cart import CartItem

class CartItemRepository:
    def __init__(self, db: Session):
        self.db = db

    # Crear un item en un carrito
    def create_item(self, cart_id: int, product_id: uuid.UUID, quantity: int) -> CartItem:
        item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    # Obtener item por ID
    def get_item(self, item_id: int) -> Optional[CartItem]:
        return self.db.query(CartItem).filter(CartItem.id == item_id).first()

    # Listar items de un carrito
    def list_items_by_cart(self, cart_id: int) -> List[CartItem]:
        return self.db.query(CartItem).filter(CartItem.cart_id == cart_id).all()

    # Actualizar cantidad de un item
    def update_quantity(self, item: CartItem, quantity: int) -> CartItem:
        item.quantity = quantity
        self.db.commit()
        self.db.refresh(item)
        return item

    # Eliminar un item
    def delete_item(self, item: CartItem):
        self.db.delete(item)
        self.db.commit()
