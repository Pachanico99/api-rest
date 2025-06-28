# models/cart_item.py

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database.database import Base
import uuid

class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.cart_id"))
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("products.product_id"))
    quantity: Mapped[int]

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")  # si luego querés acceder al nombre, stock, etc.
