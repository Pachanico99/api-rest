# carrito_dto.py
# DTOs para Carrito e ItemCarrito
from pydantic import BaseModel
from typing import List

class ItemCarritoDTO(BaseModel):
    producto_id: int
    cantidad: int

class CarritoDTO(BaseModel):
    user_id: int
    carrito_id: int
    items: List[ItemCarritoDTO]

    class Config:
        orm_mode = True
