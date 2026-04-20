from __future__ import annotations

from math import sqrt


def impermanent_loss_from_price_ratio(price_ratio: float) -> float:
    if price_ratio <= 0:
        raise ValueError("price_ratio must be positive")
    return 2 * sqrt(price_ratio) / (1 + price_ratio) - 1


def impermanent_loss_pct(initial_price: float, current_price: float) -> float | None:
    if initial_price <= 0 or current_price <= 0:
        return None
    ratio = current_price / initial_price
    return impermanent_loss_from_price_ratio(ratio) * 100

