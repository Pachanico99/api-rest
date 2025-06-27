from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.src.product.service.product_service import ProductService
from app.src.product.dto.product_dto import Product, ProductCreate

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=Product, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return ProductService(db).create_product(product)

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return ProductService(db).get_product(product_id)