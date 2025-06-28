from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List
from app.database.database import Base
from app.src.cart_item.model.cart_item import CartItem

class Cart(Base):
    __tablename__ = "carts"

    cart_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(index=True)
    operations_count: Mapped[int] = mapped_column(default=0)
    last_modified: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    items: Mapped[List["CartItem"]] = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
