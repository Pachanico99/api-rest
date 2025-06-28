# carrito_modelo.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# Modelo de Carrito para la base de datos
# Relacion entre usuario y carrito
class Carrito(Base):
    __tablename__ = "carritos"
    carrito_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    cantidad_operaciones = Column(Integer, default=0)
    ultima_modificacion = Column(DateTime, default=datetime.utcnow)
    items = relationship("ItemCarrito", back_populates="carrito", cascade="all, delete-orphan")

# Modelo de ItemCarrito para la base de datos
# Relacion entre carrito y producto
class ItemCarrito(Base):
    __tablename__ = "items_carrito"
    id = Column(Integer, primary_key=True, index=True)
    carrito_id = Column(Integer, ForeignKey("carritos.carrito_id"))
    producto_id = Column(Integer)
    cantidad = Column(Integer)
    carrito = relationship("Carrito", back_populates="items")
