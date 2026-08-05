from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Product(BaseModel):
    sku: str
    name: str
    category: str
    price: float
    stock_quantity: int

class OrderItem(BaseModel):
    sku: str
    quantity: int

class Order(BaseModel):
    order_id: str
    items: List[OrderItem]
    status: str = "pending"
    total_amount: float = 0.0
    created_at: datetime = Field(default_factory=datetime.now)
