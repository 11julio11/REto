"""
Tests unitarios para la API del Reto.

Día 4: CI/CD con Testing Automático.
Estos tests corren en el pipeline ANTES del build de imagen.
Si fallan, el merge se bloquea.
"""

from fastapi.testclient import TestClient

from main import app, items_db


client = TestClient(app)


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def setup_function():
    """Limpia la 'base de datos' antes de cada test."""
    items_db.clear()


# ──────────────────────────────────────────────
# Tests: Health Check
# ──────────────────────────────────────────────

def test_health_check_returns_200():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "reto-api"


def test_health_check_has_version():
    response = client.get("/")
    data = response.json()
    assert "version" in data


# ──────────────────────────────────────────────
# Tests: Crear items
# ──────────────────────────────────────────────

def test_create_item_returns_201():
    response = client.post("/items", json={
        "name": "Laptop",
        "description": "MacBook Pro M3",
        "price": 2499.99,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 2499.99
    assert "id" in data
    assert "created_at" in data


def test_create_item_without_description():
    response = client.post("/items", json={
        "name": "Mouse",
        "price": 29.99,
    })
    assert response.status_code == 201
    data = response.json()
    assert data["description"] is None


def test_create_item_invalid_payload_returns_422():
    # Falta el campo 'price' que es requerido
    response = client.post("/items", json={
        "name": "Teclado",
    })
    assert response.status_code == 422


# ──────────────────────────────────────────────
# Tests: Listar items
# ──────────────────────────────────────────────

def test_list_items_empty():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_list_items_after_creation():
    # Crear 2 items
    client.post("/items", json={"name": "Item 1", "price": 10.0})
    client.post("/items", json={"name": "Item 2", "price": 20.0})

    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


# ──────────────────────────────────────────────
# Tests: Obtener item por ID
# ──────────────────────────────────────────────

def test_get_item_by_id():
    # Crear un item
    create_resp = client.post("/items", json={
        "name": "Monitor",
        "price": 599.99,
    })
    item_id = create_resp.json()["id"]

    # Obtenerlo
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Monitor"


def test_get_item_not_found_returns_404():
    response = client.get("/items/id-que-no-existe")
    assert response.status_code == 404
    assert "no encontrado" in response.json()["detail"]


# ──────────────────────────────────────────────
# Tests: Eliminar item
# ──────────────────────────────────────────────

def test_delete_item():
    # Crear y luego eliminar
    create_resp = client.post("/items", json={
        "name": "Borrable",
        "price": 1.0,
    })
    item_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/items/{item_id}")
    assert delete_resp.status_code == 204

    # Verificar que ya no existe
    get_resp = client.get(f"/items/{item_id}")
    assert get_resp.status_code == 404


def test_delete_item_not_found_returns_404():
    response = client.delete("/items/id-inexistente")
    assert response.status_code == 404
