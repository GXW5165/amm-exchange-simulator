from __future__ import annotations

from dataclasses import dataclass

from src.domain.pool import Pool
from src.domain.user import User

from .impermanent_loss import impermanent_loss_pct
from .pnl import UserPnL, summarize_user_pnl
from .record import EventRecord
from .slippage import average_slippage_pct


@dataclass
class SimulationSummary:
    total_events: int
    swap_events: int
    liquidity_events: int
    total_fees: float
    average_slippage_pct: float | None
    max_slippage_pct: float | None
    impermanent_loss_pct: float | None
    user_pnl: dict[str, UserPnL]


def summarize_records(
    records: list[EventRecord],
    initial_pool: Pool,
    current_pool: Pool,
    initial_users: dict[str, User],
    current_users: dict[str, User],
) -> SimulationSummary:
    swap_events = 0
    liquidity_events = 0
    total_fees = 0.0
    slippage_values: list[float | None] = []

    for record in records:
        if record.event_type == "swap":
            swap_events += 1
        elif record.event_type in {"add_liquidity", "remove_liquidity"}:
            liquidity_events += 1

        total_fees += float(record.fee or 0.0)
        slippage_values.append(record.slippage_pct)

    filtered_slippage = [value for value in slippage_values if value is not None]
    max_slippage = max(filtered_slippage) if filtered_slippage else None
    current_price = current_pool.spot_price
    initial_price = initial_pool.spot_price

    return SimulationSummary(
        total_events=len(records),
        swap_events=swap_events,
        liquidity_events=liquidity_events,
        total_fees=total_fees,
        average_slippage_pct=average_slippage_pct(slippage_values),
        max_slippage_pct=max_slippage,
        impermanent_loss_pct=impermanent_loss_pct(initial_price, current_price),
        user_pnl=summarize_user_pnl(
            initial_users=initial_users,
            current_users=current_users,
            pool=current_pool,
            price_y_per_x=current_price,
        ),
    )
