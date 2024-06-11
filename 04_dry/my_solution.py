from decimal import Decimal
from dataclasses import dataclass
from typing import Iterable
from abc import ABC, abstractmethod

@dataclass
class Item:
    name: str
    price: Decimal


class Order(ABC):
    def __init__(self, id: int, customer_email: str):
        self.id = id
        self.customer_email = customer_email
    
    @abstractmethod
    def process_order(self):
        pass

class OnlineOrder(Order):
    def process_order(self):
        print("Processing online order...")
        print(generate_order_confirmation_email(self))
        print("Shipping the order...")
        print(generate_order_shipping_notification(self))
        print("Order processed successfully.")

class InStoreOrder(Order):
    def process_order(self):
        print("Processing in-store order...")
        print(generate_order_confirmation_email(self))
        print("Order ready for pickup.")
        print("Order processed successfully.")    

@dataclass
class Email:
    body: str
    subject: str
    recipient: str
    sender: str


def calculate_total_price(items: Iterable[Item]) -> Decimal:
    total_price = Decimal(sum(item.price for item in items))
    return total_price


def calculate_discounted_price(items: Iterable[Item], discount: Decimal) -> Decimal:
    total_price = calculate_total_price(items)
    discounted_price = total_price - (total_price * discount)
    return discounted_price


def generate_order_confirmation_email(order: Order) -> Email:
    return Email(
        body=f"Thank you for your order! Your order #{order.id} has been confirmed.",
        subject="Order Confirmation",
        recipient=order.customer_email,
        sender="sales@webshop.com",
    )


def generate_order_shipping_notification(order: Order) -> Email:
    return Email(
        body=f"Good news! Your order #{order.id} has been shipped and is on its way.",
        subject="Order Shipped",
        recipient=order.customer_email,
        sender="sales@webshop.com",
    )


def main() -> None:
    items = [
        Item(name="T-Shirt", price=Decimal("19.99")),
        Item(name="Jeans", price=Decimal("49.99")),
        Item(name="Shoes", price=Decimal("79.99")),
    ]

    online_order = OnlineOrder(
        id=123, customer_email="sarah@gmail.com"
    )

    total_price = calculate_total_price(items)
    print("Total price:", total_price)

    discounted_price = calculate_discounted_price(items, Decimal("0.1"))
    print("Discounted price:", discounted_price)

    online_order.process_order()

    in_store_order = InStoreOrder(
        id=456, customer_email="john@gmail.com"
    )

    in_store_order.process_order()


if __name__ == "__main__":
    main()
