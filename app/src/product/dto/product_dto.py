import uuid
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: uuid.UUID

    class Config:
        orm_mode = True