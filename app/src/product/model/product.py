from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID  # Solo si usás PostgreSQL, si no, omití
from app.database.database import Base
import uuid

class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        index=True,
        name="product_id",
        default=uuid.uuid4,  # Genera UUID automáticamente
        unique=True
    )
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
