# producto_repositorio.py
from sqlalchemy.orm import Session
from app.producto.modelo.producto_modelo import Producto

# Repositorio para operaciones con productos
class ProductoRepositorio:
    @staticmethod
    def obtener_todos(db: Session):
        return db.query(Producto).all()

    @staticmethod
    def obtener_producto_por_id(db: Session, producto_id):
        return db.query(Producto).filter_by(producto_id=producto_id).first()
    
    @staticmethod
    def obtener_stock(db: Session, producto_id):
        return db.query(Producto).filter_by(producto_id=producto_id).first().stock
    