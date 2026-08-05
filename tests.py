import pytest
from fastapi.testclient import TestClient
from api import app
from models import Product, OrderItem

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_data():
    # Clear and reset for each test if needed
    client.post("/products", json={"sku": "A1", "name": "Laptop Pro", "category": "Electronics", "price": 1000, "stock_quantity": 5})
    client.post("/products", json={"sku": "B2", "name": "Office Chair", "category": "Furniture", "price": 200, "stock_quantity": 10})

def test_search_api_is_case_insensitive():
    response = client.get("/products/search?query=laptop")
    assert response.status_code == 200
    assert len(response.json()["results"]) == 1
    assert response.json()["results"][0]["sku"] == "A1"

def test_order_stock_fail_atomically():
    # Attempting to order 10 Laptops (only 5 exist) should fail
    response = client.post("/orders", json=[
        {"sku": "B2", "quantity": 1},
        {"sku": "A1", "quantity": 10}
    ])
    assert response.status_code == 400
    
    # Verify stock was NOT deducted for the first item either
    search = client.get("/products/search?query=Chair")
    assert search.json()["results"][0]["stock_quantity"] == 10

def test_invalid_sku_returns_error():
    response = client.post("/orders", json=[{"sku": "FAKE", "quantity": 1}])
    assert response.status_code == 400
