# main.py
# Punto de entrada de la aplicación FastAPI
from fastapi import FastAPI
from app.producto.controlador.producto_controlador import router as producto_router
from app.carrito.controlador.carrito_controlador import router as carrito_router
from app.pago.controlador.pago_controlador import router as pago_router
from app.database import Base, engine

# Crear las tablas automáticamente al iniciar la app
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API REST Carrito de Tienda de Ropa")

app.include_router(producto_router)
app.include_router(carrito_router)
app.include_router(pago_router)
