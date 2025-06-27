from sqlalchemy.orm import Mapped, mapped_column
from app.database.database import Base
from uuid import UUID

class Product(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, name="product_id")
    name: Mapped[str] = mapped_column(index=True)
    stock: Mapped[int]

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_stock(self):
        return self.stock

    def set_id(self, id):
        self.id = id

    def set_name(self, name):
        self.name = name

    def set_stock(self, stock):
        self.stock = stock