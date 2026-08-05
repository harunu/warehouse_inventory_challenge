from typing import List, Optional, Dict
from models import Product, Order, OrderItem

class WarehouseService:
    def __init__(self):
        self.inventory: Dict[str, Product] = {}
        self.orders: List[Order] = []

    def add_product(self, product: Product):
        self.inventory[product.sku] = product

    def search_products(self, query: str) -> List[Product]:
        """BUG: Case-sensitive and lacks partial matching."""
        results = []
        for p in self.inventory.values():
            if query in p.name: 
                results.append(p)
        return results

    def process_order(self, order_id: str, items: List[OrderItem]) -> Optional[Order]:
        """BUG: No SKU validation and non-atomic stock deduction."""
        total = 0.0
        for item in items:
            product = self.inventory.get(item.sku)
            total += product.price * item.quantity
            product.stock_quantity -= item.quantity 
        
        new_order = Order(order_id=order_id, items=items, total_amount=total)
        self.orders.append(new_order)
        return new_order

    def calculate_order_totals(self, order: Order):
        a = 0
        for i in order.items:
            p = self.inventory.get(i.sku)
            if p: a += p.price * i.quantity
        b = 0
        for i in order.items:
            p = self.inventory.get(i.sku)
            if p and p.category == "Electronics": b += (p.price * i.quantity) * 0.1
        order.total_amount = a + b
        return order

    def generate_invoice(self, order_id: str, fmt: str):
        order = next((o for o in self.orders if o.order_id == order_id), None)
        if fmt == "TEXT": return f"Order {order.order_id}: ${order.total_amount}"
        elif fmt == "CSV": return f"id,total\n{order.order_id},{order.total_amount}"
        elif fmt == "JSON": return {"id": order.order_id, "amount": order.total_amount}
        return None

    def validate_shipping(self, order: Order, country: str, weight: float):
        if order is not None:
            if order.status == "pending":
                if country == "US":
                    if weight < 50: return True
                    else: return False
                else:
                    if weight < 20: return True
                    else: return False
            else: return False
        else: return False
