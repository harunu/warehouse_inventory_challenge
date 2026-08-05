from fastapi import FastAPI, HTTPException, Query
import uuid
from typing import List

from models import Product, Order, OrderItem
from service import WarehouseService

app = FastAPI(title="Warehouse Inventory API")

# Initialize services
service = WarehouseService()

@app.post("/products", status_code=201)
def add_product(product: Product):
    service.add_product(product)
    return {"message": "Product added", "sku": product.sku}

@app.get("/products/search")
def search_products(query: str = Query(..., min_length=1)):
    results = service.search_products(query)
    return {"results": results}

@app.post("/orders", status_code=201)
def create_order(items: List[OrderItem]):
    order_id = str(uuid.uuid4())
    order = service.process_order(order_id, items)
    if not order:
        raise HTTPException(status_code=400, detail="Order could not be processed (check stock or SKUs)")
    return order

@app.get("/orders/{order_id}/invoice")
def get_invoice(order_id: str, fmt: str = "JSON"):
    invoice = service.generate_invoice(order_id, fmt)
    if not invoice:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"invoice": invoice}
