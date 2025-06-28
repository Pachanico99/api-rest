# producto_controlador.py
# Controlador de productos para FastAPI
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.producto.dto.producto_dto import ProductoDTO
from app.producto.servicios.producto_servicio import ProductoServicio
from app.producto.modelo.producto_modelo import Producto

router = APIRouter(prefix="/productos", tags=["Productos"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ProductoDTO])
def listar_productos(db: Session = Depends(get_db)):
    """Devuelve la lista de productos."""
    return ProductoServicio.listar_productos(db)

@router.get("/{producto_id}", response_model=ProductoDTO)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    """Devuelve un producto por su id."""
    producto = ProductoServicio.obtener_producto_por_id(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/", response_model=ProductoDTO)
def crear_producto(producto: ProductoDTO, db: Session = Depends(get_db)):
    """Crea un nuevo producto."""
    nuevo = Producto(producto_id=producto.producto_id, nombre=producto.nombre, stock=producto.stock)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
