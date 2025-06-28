# producto_dto.py
# DTO de Producto
from pydantic import BaseModel

class ProductoDTO(BaseModel):
    producto_id: int
    nombre: str
    stock: int

    class Config:
        orm_mode = True
