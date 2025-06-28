# producto_servicio.py
from sqlalchemy.orm import Session
from app.producto.repositorio.producto_repositorio import ProductoRepositorio

# Servicio de productos
class ProductoServicio:
    @staticmethod
    def listar_productos(db: Session):
        return ProductoRepositorio.obtener_todos(db)

    @staticmethod
    def obtener_producto_por_id(db: Session, producto_id: int):
        return ProductoRepositorio.obtener_producto_por_id(db, producto_id)
    
    @staticmethod
    def obtener_stock(db: Session, producto_id: int):
        return ProductoRepositorio.obtener_stock(db, producto_id)
