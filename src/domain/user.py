from dataclasses import dataclass


@dataclass
class User:
    user_id: str
    balance_x: float = 0.0
    balance_y: float = 0.0
    lp_shares: float = 0.0

    def deposit_x(self, amount: float) -> None:
        self.balance_x += amount

    def deposit_y(self, amount: float) -> None:
        self.balance_y += amount

    def withdraw_x(self, amount: float) -> None:
        self.balance_x -= amount

    def withdraw_y(self, amount: float) -> None:
        self.balance_y -= amount
