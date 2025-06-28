# producto_modelo.py
from sqlalchemy import Column, Integer, String
from app.database import Base

# Modelo de Producto para la base de datos
class Producto(Base):
    __tablename__ = "productos"
    producto_id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
