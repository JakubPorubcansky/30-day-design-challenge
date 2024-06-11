from decimal import Decimal

def process_payment(total: Decimal) -> None:
    device_id = input("Please enter your Google Pay device ID: ")
    device_id_masked = device_id[-4:].rjust(len(device_id), "*")
    print(
        f"Processing Google Pay payment of ${total:.2f} with device ID {device_id_masked}..."
    )

def payment_method_name():
    return "google"

