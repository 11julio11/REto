"""
Tests unitarios para la API del Reto refactorizada a Clean Architecture.

Día 8: Usamos Inyección de Dependencias.
"""

from fastapi.testclient import TestClient
from main import app
from repository.memory_repository import db_instance, user_db_instance

client = TestClient(app)


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def setup_function():
    """Limpia las 'bases de datos' antes de cada test para no tener contaminación."""
    db_instance._db.clear()
    user_db_instance._users.clear()


# ──────────────────────────────────────────────
# Tests: Health Check
# ──────────────────────────────────────────────

def test_health_check_returns_200():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["arch"] == "clean-architecture"

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
    create_resp = client.post("/items", json={
        "name": "Monitor",
        "price": 599.99,
    })
    item_id = create_resp.json()["id"]

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
    create_resp = client.post("/items", json={
        "name": "Borrable",
        "price": 1.0,
    })
    item_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/items/{item_id}")
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/items/{item_id}")
    assert get_resp.status_code == 404


def test_delete_item_not_found_returns_404():
    response = client.delete("/items/id-inexistente")
    assert response.status_code == 404

# ──────────────────────────────────────────────
# Tests: Async Workers Dispatch (Día 9)
# ──────────────────────────────────────────────

def test_process_item_async_accepted():
    # 1. Crear item para procesar
    create_resp = client.post("/items", json={
        "name": "Servidor",
        "price": 1000.0,
    })
    item_id = create_resp.json()["id"]

    # 2. Despachar
    response = client.post(f"/items/{item_id}/process")
    assert response.status_code == 202
    assert "aceptado" in response.json()["message"]

# ──────────────────────────────────────────────
# Tests: Authentication (Día 26)
# ──────────────────────────────────────────────

def test_register_and_login_success():
    # 1. Registro
    reg_resp = client.post("/auth/register", json={"username": "testuser", "password": "password123"})
    assert reg_resp.status_code == 201
    
    # 2. Login
    login_resp = client.post("/auth/login", data={"username": "testuser", "password": "password123"})
    assert login_resp.status_code == 200
    data = login_resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password_returns_401():
    client.post("/auth/register", json={"username": "badpass", "password": "correctpassword"})
    
    response = client.post("/auth/login", data={"username": "badpass", "password": "wrongpassword"})
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

def test_login_nonexistent_user_returns_401():
    response = client.post("/auth/login", data={"username": "ghost", "password": "password"})
    assert response.status_code == 401

def test_protected_route_without_token_returns_401():
    response = client.get("/items")
    assert response.status_code == 401

def test_protected_route_with_valid_token():
    # Setup: Register, Login, Get Token
    client.post("/auth/register", json={"username": "authuser", "password": "password123"})
    login_resp = client.post("/auth/login", data={"username": "authuser", "password": "password123"})
    token = login_resp.json()["access_token"]
    
    # Access protected route
    response = client.get("/items", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
