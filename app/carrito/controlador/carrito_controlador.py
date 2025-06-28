# carrito_controlador.py
# Controlador de carritos para FastAPI
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.carrito.dto.carrito_dto import CarritoDTO, ItemCarritoDTO
from app.carrito.servicios.carrito_servicio import CarritoServicio

router = APIRouter(prefix="/carritos", tags=["Carritos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{carrito_id}", response_model=CarritoDTO)
def obtener_carrito(carrito_id: int, db: Session = Depends(get_db)):
    # Limpiar carritos inactivos antes de devolver el carrito solicitado
    CarritoServicio.limpiar_carritos_inactivos(db)
    carrito = CarritoServicio.obtener_carrito(db, carrito_id)
    if not carrito:
        raise HTTPException(status_code=404, detail="Carrito no encontrado")
    return carrito

@router.post("/", response_model=CarritoDTO)
def crear_carrito(user_id: int, db: Session = Depends(get_db)):
    try:
        carrito = CarritoServicio.crear_carrito(db, user_id)
        return carrito
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{carrito_id}")
def eliminar_carrito(carrito_id: int, db: Session = Depends(get_db)):
    CarritoServicio.eliminar_carrito(db, carrito_id)
    return {"mensaje": "Carrito eliminado"}

@router.put("/{carrito_id}", response_model=CarritoDTO)
def sobreescribir_carrito(carrito_id: int, carrito: CarritoDTO, db: Session = Depends(get_db)):
    try:
        nuevo = CarritoServicio.sobreescribir_carrito(db, carrito_id, [item.dict() for item in carrito.items])
        return nuevo
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{carrito_id}", response_model=CarritoDTO)
def agregar_items(carrito_id: int, items: list[ItemCarritoDTO], db: Session = Depends(get_db)):
    try:
        nuevo = CarritoServicio.agregar_items(db, carrito_id, [item.dict() for item in items])
        return nuevo
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
