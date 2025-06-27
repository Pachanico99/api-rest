from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class CartItem(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, description="Quantity must be greater than zero.")

class CartCreate(BaseModel):
    user_id: int

class Cart(BaseModel):
    cart_id: int
    user_id: int
    items: List[CartItem]
    operations_count: int
    last_modified: datetime

class PaymentResponse(BaseModel):
    tracking_id: int