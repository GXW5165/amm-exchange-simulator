from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from .exceptions import InsufficientBalanceError, InsufficientLiquidityError


@dataclass
class Pool:
    reserve_x: float
    reserve_y: float
    fee_rate: float = 0.003
    total_lp_shares: float = 0.0

    @property
    def spot_price(self) -> float:
        if self.reserve_x <= 0:
            return float("inf")
        return self.reserve_y / self.reserve_x

    def add_liquidity(self, amount_x: float, amount_y: float) -> tuple[float, float, float]:
        if amount_x <= 0 or amount_y <= 0:
            raise InsufficientBalanceError("Liquidity amounts must be positive")

        if self.reserve_x <= 0 or self.reserve_y <= 0 or self.total_lp_shares <= 0:
            minted_shares = sqrt(amount_x * amount_y)
            self.reserve_x += amount_x
            self.reserve_y += amount_y
            self.total_lp_shares += minted_shares
            return amount_x, amount_y, minted_shares

        share_ratio = min(amount_x / self.reserve_x, amount_y / self.reserve_y)
        if share_ratio <= 0:
            raise InsufficientBalanceError("Invalid liquidity ratio")

        consumed_x = self.reserve_x * share_ratio
        consumed_y = self.reserve_y * share_ratio
        minted_shares = self.total_lp_shares * share_ratio
        self.reserve_x += consumed_x
        self.reserve_y += consumed_y
        self.total_lp_shares += minted_shares
        return consumed_x, consumed_y, minted_shares

    def remove_liquidity(self, lp_share: float) -> tuple[float, float]:
        if lp_share <= 0:
            raise InsufficientLiquidityError("LP share must be positive")
        if self.total_lp_shares <= 0 or lp_share > self.total_lp_shares:
            raise InsufficientLiquidityError("Not enough liquidity")

        share_ratio = lp_share / self.total_lp_shares
        amount_x = self.reserve_x * share_ratio
        amount_y = self.reserve_y * share_ratio
        self.reserve_x -= amount_x
        self.reserve_y -= amount_y
        self.total_lp_shares -= lp_share
        return amount_x, amount_y

    def swap(self, direction: str, amount_in: float) -> tuple[float, float]:
        if amount_in <= 0:
            raise InsufficientBalanceError("Swap amount must be positive")

        fee = amount_in * self.fee_rate
        effective_in = amount_in - fee
        k = self.reserve_x * self.reserve_y

        if direction == "x_to_y":
            new_reserve_x = self.reserve_x + effective_in
            amount_out = self.reserve_y - (k / new_reserve_x)
            self.reserve_x += amount_in
            self.reserve_y -= amount_out
            return amount_out, fee

        if direction == "y_to_x":
            new_reserve_y = self.reserve_y + effective_in
            amount_out = self.reserve_x - (k / new_reserve_y)
            self.reserve_y += amount_in
            self.reserve_x -= amount_out
            return amount_out, fee

        raise ValueError(f"Unsupported swap direction: {direction}")
