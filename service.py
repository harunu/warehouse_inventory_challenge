from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from models import Product, Order, OrderItem

ELECTRONICS_SURCHARGE_RATE = 0.1


class InvoiceFormatter(ABC):
    @abstractmethod
    def format(self, order: Order) -> object:
        ...


class TextInvoiceFormatter(InvoiceFormatter):
    def format(self, order: Order) -> str:
        return f"Order {order.order_id}: ${order.total_amount}"


class CsvInvoiceFormatter(InvoiceFormatter):
    def format(self, order: Order) -> str:
        return f"id,total\n{order.order_id},{order.total_amount}"


class JsonInvoiceFormatter(InvoiceFormatter):
    def format(self, order: Order) -> dict:
        return {"id": order.order_id, "amount": order.total_amount}


INVOICE_FORMATTERS: Dict[str, InvoiceFormatter] = {
    "TEXT": TextInvoiceFormatter(),
    "CSV": CsvInvoiceFormatter(),
    "JSON": JsonInvoiceFormatter(),
}


class WarehouseService:
    def __init__(self):
        self.inventory: Dict[str, Product] = {}
        self.orders: List[Order] = []

    def add_product(self, product: Product):
        self.inventory[product.sku] = product

    def search_products(self, query: str) -> List[Product]:
        query_lower = query.lower()
        results = []
        for p in self.inventory.values():
            if query_lower in p.name.lower():
                results.append(p)
        return results

    def process_order(self, order_id: str, items: List[OrderItem]) -> Optional[Order]:
        total = 0.0
        for item in items:
            product = self.inventory.get(item.sku)
            if product is None or product.stock_quantity < item.quantity:
                return None
            total += product.price * item.quantity

        for item in items:
            self.inventory[item.sku].stock_quantity -= item.quantity

        new_order = Order(order_id=order_id, items=items, total_amount=total)
        self.orders.append(new_order)
        return new_order

    def calculate_order_totals(self, order: Order):
        subtotal = 0.0
        surcharge = 0.0
        for item in order.items:
            product = self.inventory.get(item.sku)
            if product is None:
                continue
            line_total = product.price * item.quantity
            subtotal += line_total
            if product.category == "Electronics":
                surcharge += line_total * ELECTRONICS_SURCHARGE_RATE
        order.total_amount = subtotal + surcharge
        return order

    def generate_invoice(self, order_id: str, fmt: str):
        order = next((o for o in self.orders if o.order_id == order_id), None)
        if order is None:
            return None
        formatter = INVOICE_FORMATTERS.get(fmt)
        if formatter is None:
            return None
        return formatter.format(order)

    def validate_shipping(self, order: Order, country: str, weight: float) -> bool:
        if order is None or order.status != "pending":
            return False
        max_weight = 50 if country == "US" else 20
        return weight < max_weight
