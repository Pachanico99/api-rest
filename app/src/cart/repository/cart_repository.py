from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.src.cart.model.cart import Cart

class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    # Crear un carrito nuevo
    def create_cart(self, user_id: int) -> Cart:
        cart = Cart(user_id=user_id, operations_count=0)
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return cart

    # Obtener carrito por ID
    def get_cart(self, cart_id: int) -> Optional[Cart]:
        return self.db.query(Cart).filter(Cart.cart_id == cart_id).first()

    # Listar todos los carritos (opcional)
    def list_carts(self) -> List[Cart]:
        return self.db.query(Cart).all()

    # Incrementar contador operaciones y actualizar fecha
    def update_operations(self, cart: Cart):
        cart.operations_count += 1
        cart.last_modified = datetime.utcnow()
        self.db.commit()
        self.db.refresh(cart)
        return cart

    # Eliminar carrito
    def delete_cart(self, cart: Cart):
        self.db.delete(cart)
        self.db.commit()

