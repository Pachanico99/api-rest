from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.src.product.service.product_service import ProductService
from app.src.product.dto.product_dto import Product, ProductCreate
import uuid

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=Product, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return ProductService(db).create_product(product)

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: uuid.UUID, db: Session = Depends(get_db)):
    return ProductService(db).get_product(product_id)

@router.get("", response_model=List[Product])
def get_all_products(db: Session = Depends(get_db)):
    return ProductService(db).get_all_products()
