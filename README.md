# API REST - Carrito de compras

Este proyecto implementa una API REST para la gestión de carritos de compra y productos, usando FastAPI, SQLAlchemy y SQLite. La arquitectura sigue el patrón scream (MVC por dominio).

## Requisitos
- Python 3.10+
- (Opcional) Se recomienda usar un entorno virtual (venv)

## Instalación y configuración

1. **Clona el repositorio o descarga el código.**

2. **Crea y activa un entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Levanta el servidor FastAPI:**
   ```bash
   uvicorn app.main:app --reload
   ```
   La API estará disponible en: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Estructura del proyecto
- `app/` - Código fuente de la aplicación (por dominio: producto, carrito, pago)
- `tests/` - Tests unitarios
- `requirements.txt` - Dependencias

## Endpoints principales
- `/productos/` - Gestión de productos (listar, crear, obtener por id)
- `/carritos/` - Gestión de carritos (crear, modificar, eliminar, agregar ítems, etc.)
- `/pago/{carrito_id}/` - Pago de carrito

## Ejecutar los tests unitarios

Asegúrate de tener el entorno virtual activo y las dependencias instaladas.

```bash
pytest tests/test_carrito.py
```

Esto ejecutará los tests de unidad para la lógica de carritos, incluyendo casos de fraude, stock, operaciones y pago.

---