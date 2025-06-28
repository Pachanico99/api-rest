# carrito_repositorio.py
# Repositorio para operaciones con carritos
from sqlalchemy.orm import Session
from app.carrito.modelo.carrito_modelo import Carrito

class CarritoRepositorio:
    @staticmethod
    def obtener_por_id(db: Session, carrito_id: int):
        return db.query(Carrito).filter(Carrito.carrito_id == carrito_id).first()

    @staticmethod
    def obtener_por_usuario(db: Session, user_id: int):
        return db.query(Carrito).filter(Carrito.user_id == user_id).first()

    @staticmethod
    def crear(db: Session, carrito: Carrito):
        db.add(carrito)
        db.commit()
        db.refresh(carrito)
        return carrito

    @staticmethod
    def eliminar(db: Session, carrito: Carrito):
        db.delete(carrito)
        db.commit()

    @staticmethod
    def actualizar(db: Session, carrito: Carrito):
        db.commit()
        db.refresh(carrito)
        return carrito
