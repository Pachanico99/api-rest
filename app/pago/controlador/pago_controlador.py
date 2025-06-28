# pago_controlador.py
# Controlador para el pago de carritos
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.carrito.servicios.carrito_servicio import CarritoServicio
from app.carrito.repositorio.carrito_repositorio import CarritoRepositorio
from app.producto.modelo.producto_modelo import Producto
import random

router = APIRouter(prefix="/pago", tags=["Pago"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{carrito_id}/")
def pagar_carrito(carrito_id: int, db: Session = Depends(get_db)):
    carrito = CarritoRepositorio.obtener_por_id(db, carrito_id)
    if not carrito:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    try:
        CarritoServicio.validar_stock_y_fraude(db, carrito)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # Restar stock
    for item in carrito.items:
        producto = db.query(Producto).filter(Producto.producto_id == item.producto_id).first()
        if producto:
            if producto.stock < item.cantidad:
                raise HTTPException(status_code=400, detail=f"Stock insuficiente para producto {producto.producto_id}")
            producto.stock -= item.cantidad
    # Eliminar carrito
    CarritoRepositorio.eliminar(db, carrito)
    seguimiento_id = random.randint(100000, 999999)
    print(f"Carrito {carrito_id} pagado. Número de seguimiento: {seguimiento_id}")
    return {"seguimiento_id": seguimiento_id}
