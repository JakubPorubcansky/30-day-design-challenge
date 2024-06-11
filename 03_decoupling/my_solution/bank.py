from typing import Protocol
from dataclasses import dataclass
from decimal import Decimal


class IPaymentService(Protocol):
    def process_payment(self, amount: Decimal) -> None:
        ...

    def process_payout(self, amount: Decimal) -> None:
        ...

class IAccount(Protocol):
    def deposit(self, amount: Decimal) -> None:
        ...

    def withdraw(self, amount: Decimal) -> None:
        ...

@dataclass
class SavingsAccount:
    account_number: str
    balance: Decimal

    def deposit(self, amount: Decimal) -> None:
        print(f"Depositing {amount} into Savings Account {self.account_number}.")
        self.balance += amount
    
    def withdraw(self, amount: Decimal) -> None:
        print(f"Withdrawing {amount} from Savings Account {self.account_number}.")
        self.balance -= amount


@dataclass
class CheckingAccount:
    account_number: str
    balance: Decimal

    def deposit(self, amount: Decimal) -> None:
        print(f"Depositing {amount} into Checking Account {self.account_number}.")
        self.balance += amount
    
    def withdraw(self, amount: Decimal) -> None:
        print(f"Withdrawing {amount} from Checking Account {self.account_number}.")
        self.balance -= amount


class BankService:
    def __init__(self, payment_service: IPaymentService) -> None:
        self.payment_service = payment_service

    def deposit(self, amount: Decimal, account: IAccount) -> None:
        account.deposit(amount)
        self.payment_service.process_payment(amount)

    def withdraw(self, amount: Decimal, account: IAccount) -> None:
        account.withdraw(amount)
        self.payment_service.process_payout(amount)
