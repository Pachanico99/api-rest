import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.cart.service import cart_service
from .test_database import override_get_db

# Sobrescribimos la dependencia de la base de datos para usar la de testing
app.dependency_overrides[get_db] = override_get_db

class TestCartLogic(unittest.TestCase):
    
    def setUp(self):
        """Se ejecuta antes de cada test."""
        self.client = TestClient(app)
        # Limpiamos los diccionarios en memoria antes de cada test para asegurar aislamiento
        cart_service.CARTS.clear()
        cart_service.USER_CART_MAP.clear()
        # Creamos productos de prueba
        self.p1 = self.client.post("/products/", json={"name": "Laptop", "stock": 10}).json()
        self.p2 = self.client.post("/products/", json={"name": "Mouse", "stock": 5}).json()

    def test_create_cart_successfully(self):
        """Verifica que un carrito se pueda crear para un nuevo usuario."""
        response = self.client.post("/carts/", json={"user_id": 100})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["user_id"], 100)
        self.assertIn("cart_id", data)

    def test_fail_to_create_second_cart_for_same_user(self):
        """Verifica que un usuario no pueda tener dos carritos activos."""
        self.client.post("/carts/", json={"user_id": 101}) # Primer carrito, exitoso
        response = self.client.post("/carts/", json={"user_id": 101}) # Segundo intento, debe fallar
        self.assertEqual(response.status_code, 409) # 409 Conflict

    def test_create_new_cart_after_payment(self):
        """Verifica que se pueda crear un nuevo carrito después de pagar el anterior."""
        user_id = 102
        # 1. Crear y pagar un carrito
        cart_res = self.client.post("/carts/", json={"user_id": user_id})
        cart_id = cart_res.json()["cart_id"]
        self.client.put(f"/carts/{cart_id}/items", json={"product_id": self.p1["product_id"], "quantity": 1})
        self.client.post(f"/carts/{cart_id}/pay")

        # 2. Intentar crear un nuevo carrito para el mismo usuario, debe ser exitoso
        response = self.client.post("/carts/", json={"user_id": user_id})
        self.assertEqual(response.status_code, 201)

    def test_stock_decremented_after_payment(self):
        """Verifica que el stock del producto se reduzca correctamente tras el pago."""
        initial_stock = self.p1["stock"]
        quantity_to_buy = 3
        
        # Crear carrito, añadir item y pagar
        cart_res = self.client.post("/carts/", json={"user_id": 103})
        cart_id = cart_res.json()["cart_id"]
        self.client.put(f"/carts/{cart_id}/items", json={"product_id": self.p1["product_id"], "quantity": quantity_to_buy})
        payment_res = self.client.post(f"/carts/{cart_id}/pay")
        self.assertEqual(payment_res.status_code, 200)

        # Verificar el nuevo stock del producto
        product_res = self.client.get(f"/products/{self.p1['product_id']}")
        final_stock = product_res.json()["stock"]
        
        self.assertEqual(final_stock, initial_stock - quantity_to_buy)

    def test_add_item_exceeding_stock(self):
        """Verifica que no se pueda añadir un ítem si no hay stock suficiente."""
        cart_res = self.client.post("/carts/", json={"user_id": 104})
        cart_id = cart_res.json()["cart_id"]
        
        response = self.client.put(f"/carts/{cart_id}/items", json={"product_id": self.p1["product_id"], "quantity": 999})
        self.assertEqual(response.status_code, 409)