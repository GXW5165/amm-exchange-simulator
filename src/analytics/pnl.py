from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass

from src.domain.pool import Pool
from src.domain.user import User


@dataclass
class UserPnL:
    user_id: str
    initial_value_in_y: float
    final_wallet_value_in_y: float
    final_total_value_in_y: float
    wallet_pnl_in_y: float
    total_pnl_in_y: float
    lp_position_value_in_y: float


def portfolio_value_in_y(user: User, price_y_per_x: float) -> float:
    return user.balance_x * price_y_per_x + user.balance_y


def lp_position_value_in_y(pool: Pool, user: User, price_y_per_x: float) -> float:
    if pool.total_lp_shares <= 0 or user.lp_shares <= 0:
        return 0.0
    share_ratio = user.lp_shares / pool.total_lp_shares
    amount_x = pool.reserve_x * share_ratio
    amount_y = pool.reserve_y * share_ratio
    return amount_x * price_y_per_x + amount_y


def summarize_user_pnl(
    initial_users: dict[str, User],
    current_users: dict[str, User],
    pool: Pool,
    price_y_per_x: float,
) -> dict[str, UserPnL]:
    summary: dict[str, UserPnL] = {}
    user_ids = set(initial_users) | set(current_users)
    for user_id in sorted(user_ids):
        initial_user = deepcopy(initial_users.get(user_id, User(user_id=user_id)))
        current_user = deepcopy(current_users.get(user_id, User(user_id=user_id)))
        initial_value = portfolio_value_in_y(initial_user, price_y_per_x)
        final_wallet_value = portfolio_value_in_y(current_user, price_y_per_x)
        lp_value = lp_position_value_in_y(pool, current_user, price_y_per_x)
        final_total_value = final_wallet_value + lp_value
        summary[user_id] = UserPnL(
            user_id=user_id,
            initial_value_in_y=initial_value,
            final_wallet_value_in_y=final_wallet_value,
            final_total_value_in_y=final_total_value,
            wallet_pnl_in_y=final_wallet_value - initial_value,
            total_pnl_in_y=final_total_value - initial_value,
            lp_position_value_in_y=lp_value,
        )
    return summary

