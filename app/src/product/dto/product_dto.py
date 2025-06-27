from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    product_id: int

    class Config:
        from_attributes = True