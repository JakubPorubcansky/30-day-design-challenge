from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Item:
    name: str
    price: Decimal
    quantity: int

    @property
    def total_price(self) -> Decimal:
        return self.price * self.quantity
    
    def update_quantity(self, new_quantity: int) -> None:
        self.quantity = new_quantity

    def update_price(self, new_price: Decimal) -> None:
        self.price = new_price


@dataclass
class ShoppingCart:
    items: list[Item] = field(default_factory=list)
    discount_code: str | None = None

    @property
    def total_price(self) -> Decimal:
        return sum(item.total_price for item in self.items)
    
    def remove_item(self, item_idx: int) -> None:
        self.items.pop(item_idx)

    def update_item(self, item_idx: int, new_quantity: int | None = None, new_price: int | None = None) -> None:
        if new_price:
            self.items[item_idx].update_price(new_price)
        if new_quantity:
            self.items[item_idx].update_quantity(new_quantity)


def main() -> None:
    # Create a shopping cart and add some items to it
    cart = ShoppingCart(
        items=[
            Item("Apple", Decimal("1.5"), 10),
            Item("Banana", Decimal("2"), 2),
            Item("Pizza", Decimal("11.90"), 5),
        ],
    )

    # Update some items' quantity and price
    cart.update_item(0, new_quantity=10)
    cart.update_item(2, new_price=Decimal("3.50"))

    # Remove an item
    cart.remove_item(1)

    # Print the cart
    print("Shopping Cart:")
    print(f"{'Item':<10}{'Price':>10}{'Qty':>7}{'Total':>13}")
    for item in cart.items:
        print(
            f"{item.name:<12}${item.price:>7.2f}{item.quantity:>7}     ${item.total_price:>7.2f}"
        )
    print("=" * 40)
    print(f"Total: ${cart.total_price:>7.2f}")


if __name__ == "__main__":
    main()
