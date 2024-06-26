from decimal import Decimal

def process_payment(total: Decimal) -> None:
    username = input("Please enter your PayPal username: ")
    password = input("Please enter your PayPal password: ")
    password_masked = len(password) * "*"
    print(
        f"Processing PayPal payment of ${total:.2f} with username {username} and password {password_masked}..."
    )

def payment_method_name():
    return "paypal"