import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.database import Base, engine
from app.src.product.controller import product_controller
from app.src.cart.controller import cart_controller
from app.src.cart.service.cart_service import cleanup_inactive_carts_task

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("INFO:     Iniciando tarea en segundo plano para limpiar carritos inactivos.")
    task = asyncio.create_task(cleanup_inactive_carts_task())
    yield
    print("INFO:     Cancelando tarea en segundo plano.")
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("INFO:     Tarea en segundo plano cancelada exitosamente.")

app = FastAPI(
    title="API de Carrito de Compras",
    description="Implementación de un sistema de carritos con reglas de negocio complejas.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(product_controller.router)
app.include_router(cart_controller.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API de Carrito de Compras"}
