# test_carrito.py
# Tests unitarios para la lógica de carritos
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app.producto.modelo.producto_modelo import Producto

client = TestClient(app)

class TestCarrito(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Crear las tablas y limpiar la base de datos
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        # Crear productos iniciales
        db.add(Producto(producto_id=1, nombre="Remera", stock=10))
        db.add(Producto(producto_id=2, nombre="Pantalón", stock=5))
        db.commit()
        db.close()

    def test_crear_carrito(self):
        response = client.post("/carritos/?user_id=1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['user_id'], 1)

    def test_no_dos_carritos_mismo_usuario(self):
        client.post("/carritos/?user_id=2")
        response = client.post("/carritos/?user_id=2")
        self.assertEqual(response.status_code, 400)

    def test_agregar_items_y_limite(self):
        # Crear carrito
        resp = client.post("/carritos/?user_id=3")
        carrito_id = resp.json()['carrito_id']
        # Agregar 16 items (fraude)
        items = [{"producto_id": 1, "cantidad": 1}] * 16
        response = client.patch(f"/carritos/{carrito_id}", json=items)
        self.assertEqual(response.status_code, 400)

    def test_limite_operaciones(self):
        resp = client.post("/carritos/?user_id=4")
        carrito_id = resp.json()['carrito_id']
        items = [{"producto_id": 1, "cantidad": 1}]
        for _ in range(20):
            response = client.patch(f"/carritos/{carrito_id}", json=items)
        # La operación 21 debe eliminar el carrito
        response = client.patch(f"/carritos/{carrito_id}", json=items)
        self.assertEqual(response.status_code, 400)

    def test_limite_producto(self):
        resp = client.post("/carritos/?user_id=5")
        carrito_id = resp.json()['carrito_id']
        # Agregar más de 10 unidades de un producto
        items = [{"producto_id": 1, "cantidad": 11}]
        response = client.patch(f"/carritos/{carrito_id}", json=items)
        self.assertEqual(response.status_code, 400)

    def test_stock_insuficiente(self):
        resp = client.post("/carritos/?user_id=6")
        carrito_id = resp.json()['carrito_id']
        items = [{"producto_id": 2, "cantidad": 6}]
        response = client.put(f"/carritos/{carrito_id}", json={"user_id": 6, "carrito_id": carrito_id, "items": items})
        print(response.json())
        self.assertEqual(response.status_code, 400)

    def test_pago_descuenta_stock(self):
        # Crear carrito y agregar items
        resp = client.post("/carritos/?user_id=7")
        carrito_id = resp.json()['carrito_id']
        items = [{"producto_id": 1, "cantidad": 2}]
        client.patch(f"/carritos/{carrito_id}", json=items)
        # Realizar pago
        response = client.get(f"/pago/{carrito_id}/")
        self.assertEqual(response.status_code, 200)
        # Verificar stock
        db = SessionLocal()
        producto = db.query(Producto).filter(Producto.producto_id == 1).first()
        self.assertEqual(producto.stock, 8)
        db.close()

    def test_puedo_recrear_carrito_tras_pago(self):
        # Crear carrito y pagar
        resp = client.post("/carritos/?user_id=8")
        carrito_id = resp.json()['carrito_id']
        client.get(f"/pago/{carrito_id}/")
        # Ahora debería poder crear otro carrito
        response = client.post("/carritos/?user_id=8")
        self.assertEqual(response.status_code, 200)

    def test_carrito_inactivo_se_elimina(self):
        import time
        # Crear carrito
        resp = client.post("/carritos/?user_id=99")
        self.assertEqual(resp.status_code, 200)
        carrito_id = resp.json()['carrito_id']
        # Esperar más de 10 segundos
        time.sleep(11)
        # Hacer GET al carrito (esto dispara la limpieza de inactivos)
        resp_get = client.get(f"/carritos/{carrito_id}")
        self.assertEqual(resp_get.status_code, 404)

if __name__ == "__main__":
    unittest.main()
