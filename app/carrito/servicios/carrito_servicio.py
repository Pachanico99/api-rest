# carrito_servicio.py
# Servicio de lógica de negocio para carritos
from sqlalchemy.orm import Session
from app.carrito.modelo.carrito_modelo import Carrito, ItemCarrito
from app.carrito.repositorio.carrito_repositorio import CarritoRepositorio
from app.producto.modelo.producto_modelo import Producto
from app.producto.servicios.producto_servicio import ProductoServicio
from datetime import datetime, timedelta

class CarritoServicio:
    LIMITE_ITEMS = 15
    LIMITE_OPERACIONES = 20
    LIMITE_PRODUCTO = 10
    TIEMPO_INACTIVIDAD_MIN = 0.166667 # 10 segundos

    @staticmethod
    def crear_carrito(db: Session, user_id: int):
        existente = CarritoRepositorio.obtener_por_usuario(db, user_id)
        if existente:
            raise Exception("Ya existe un carrito para este usuario.")
        nuevo = Carrito(user_id=user_id, cantidad_operaciones=0, ultima_modificacion=datetime.utcnow())
        return CarritoRepositorio.crear(db, nuevo)

    @staticmethod
    def obtener_carrito(db: Session, carrito_id: int):
        return CarritoRepositorio.obtener_por_id(db, carrito_id)

    @staticmethod
    def eliminar_carrito(db: Session, carrito_id: int):
        carrito = CarritoRepositorio.obtener_por_id(db, carrito_id)
        if carrito:
            CarritoRepositorio.eliminar(db, carrito)

    @staticmethod
    def sobreescribir_carrito(db: Session, carrito_id: int, items: list):
        carrito = CarritoRepositorio.obtener_por_id(db, carrito_id)
        if not carrito:
            raise Exception("Carrito no encontrado.")
        if len(items) > CarritoServicio.LIMITE_ITEMS:
            raise Exception("No puede haber más de 15 ítems en el carrito.")
        carrito.items.clear()
        CarritoServicio.agregar_items(db, carrito_id, items)
        return carrito

    @staticmethod
    def agregar_items(db: Session, carrito_id: int, items: list):
        carrito = CarritoRepositorio.obtener_por_id(db, carrito_id)
        if not carrito:
            raise Exception("Carrito no encontrado.")
        for item in items:
            if item["cantidad"] > CarritoServicio.LIMITE_PRODUCTO:
                raise Exception("No puede agregar más de 10 unidades del producto.")
            if item["cantidad"] > ProductoServicio.obtener_stock(db, item["producto_id"]):
                raise Exception("No hay stock suficiente")
            carrito.items.append(ItemCarrito(producto_id=item["producto_id"], cantidad=item["cantidad"]))
        if len(carrito.items) > CarritoServicio.LIMITE_ITEMS:
            raise Exception("No puede haber más de 15 ítems en el carrito.")
        carrito.cantidad_operaciones += 1
        carrito.ultima_modificacion = datetime.utcnow()
        if carrito.cantidad_operaciones > CarritoServicio.LIMITE_OPERACIONES:
            CarritoRepositorio.eliminar(db, carrito)
            raise Exception("Carrito eliminado por fraude (más de 20 operaciones).");
        CarritoRepositorio.actualizar(db, carrito)
        return carrito

    @staticmethod
    def limpiar_carritos_inactivos(db: Session):
        ahora = datetime.utcnow()
        carritos = db.query(Carrito).all()
        for carrito in carritos:
            if (ahora - carrito.ultima_modificacion) > timedelta(minutes=CarritoServicio.TIEMPO_INACTIVIDAD_MIN):
                CarritoRepositorio.eliminar(db, carrito)

    @staticmethod
    def validar_stock_y_fraude(db: Session, carrito: Carrito):
        productos = db.query(Producto).all()
        stock_dict = {p.producto_id: p.stock for p in productos}
        conteo = {}
        for item in carrito.items:
            conteo[item.producto_id] = conteo.get(item.producto_id, 0) + item.cantidad
        for prod_id, cantidad in conteo.items():
            if cantidad > CarritoServicio.LIMITE_PRODUCTO:
                raise Exception(f"No puede agregar más de 10 unidades del producto {prod_id}.")
            if cantidad > stock_dict.get(prod_id, 0):
                raise Exception(f"No hay suficiente stock para el producto {prod_id}.")
