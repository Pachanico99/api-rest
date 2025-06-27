from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.src.product.repository.product_repository import ProductRepository
from app.src.product.model.product import Product
from app.src.product.dto.product_dto import ProductCreate

class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)

    def create_product(self, product_create: ProductCreate) -> Product:
        if product_create.stock < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Stock cannot be negative.")
        
        product = Product(name=product_create.name, stock=product_create.stock)
        return self.repository.save(product)

    def get_product(self, product_id: int) -> Product:
        product = self.repository.find_by_id(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
        return product