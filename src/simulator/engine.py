from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.domain.exceptions import InsufficientBalanceError, InsufficientLiquidityError, InvalidEventError, PoolNotInitializedError
from src.domain.metrics import EventRecord
from src.domain.pool import Pool
from src.domain.user import User

from .event import Event, EventType
from .event_queue import EventQueue


@dataclass
class SimulationResult:
    records: list[EventRecord]
    pool: Pool
    users: dict[str, User]


class SimulatorEngine:
    def __init__(self, pool: Pool | None = None, users: dict[str, User] | None = None) -> None:
        self.pool = pool
        self.users = users or {}
        self.event_queue = EventQueue()
        self.records: list[EventRecord] = []

    def ensure_user(self, user_id: str) -> User:
        if user_id not in self.users:
            self.users[user_id] = User(user_id=user_id)
        return self.users[user_id]

    def schedule(self, event: Event) -> None:
        self.event_queue.push(event)

    def run(self, events: list[Event] | None = None) -> SimulationResult:
        if events:
            self.event_queue.extend(events)

        while not self.event_queue.empty():
            event = self.event_queue.pop()
            if event is None:
                break
            self.records.append(self.process_event(event))

        if self.pool is None:
            raise PoolNotInitializedError("Pool is not initialized")

        return SimulationResult(records=self.records, pool=self.pool, users=self.users)

    def process_event(self, event: Event) -> EventRecord:
        if self.pool is None:
            raise PoolNotInitializedError("Pool is not initialized")

        user = self.ensure_user(event.user_id)
        if event.event_type == EventType.SWAP:
            return self._process_swap(event, user)
        if event.event_type == EventType.ADD_LIQUIDITY:
            return self._process_add_liquidity(event, user)
        if event.event_type == EventType.REMOVE_LIQUIDITY:
            return self._process_remove_liquidity(event, user)
        raise InvalidEventError(f"Unsupported event type: {event.event_type}")

    def _process_swap(self, event: Event, user: User) -> EventRecord:
        direction = str(event.payload.get("direction", ""))
        amount_in = float(event.payload.get("amount_in", 0.0))
        if direction == "x_to_y":
            if user.balance_x < amount_in:
                raise InsufficientBalanceError("User has insufficient Token X")
            amount_out, fee = self.pool.swap(direction, amount_in)
            user.balance_x -= amount_in
            user.balance_y += amount_out
        elif direction == "y_to_x":
            if user.balance_y < amount_in:
                raise InsufficientBalanceError("User has insufficient Token Y")
            amount_out, fee = self.pool.swap(direction, amount_in)
            user.balance_y -= amount_in
            user.balance_x += amount_out
        else:
            raise InvalidEventError("Swap direction must be x_to_y or y_to_x")

        spot_price = self.pool.spot_price
        execution_price = amount_out / amount_in if amount_in else None
        slippage_pct = None if spot_price in (0.0, float("inf")) or execution_price is None else abs(execution_price - spot_price) / spot_price * 100
        return self._build_record(
            event=event,
            user_id=user.user_id,
            event_type=event.event_type.value,
            direction=direction,
            amount_in=amount_in,
            amount_out=amount_out,
            fee=fee,
            spot_price=spot_price,
            execution_price=execution_price,
            slippage_pct=slippage_pct,
        )

    def _process_add_liquidity(self, event: Event, user: User) -> EventRecord:
        amount_x = float(event.payload.get("amount_x", 0.0))
        amount_y = float(event.payload.get("amount_y", 0.0))
        if user.balance_x < amount_x or user.balance_y < amount_y:
            raise InsufficientBalanceError("User has insufficient balance for liquidity provision")

        consumed_x, consumed_y, minted_shares = self.pool.add_liquidity(amount_x, amount_y)
        user.balance_x -= consumed_x
        user.balance_y -= consumed_y
        user.lp_shares += minted_shares

        return self._build_record(
            event=event,
            user_id=user.user_id,
            event_type=event.event_type.value,
            amount_in=consumed_x,
            amount_out=consumed_y,
            fee=0.0,
            spot_price=self.pool.spot_price,
            execution_price=None,
            slippage_pct=None,
        )

    def _process_remove_liquidity(self, event: Event, user: User) -> EventRecord:
        lp_share = float(event.payload.get("lp_share", 0.0))
        if user.lp_shares < lp_share:
            raise InsufficientLiquidityError("User does not own enough LP shares")

        amount_x, amount_y = self.pool.remove_liquidity(lp_share)
        user.lp_shares -= lp_share
        user.balance_x += amount_x
        user.balance_y += amount_y

        return self._build_record(
            event=event,
            user_id=user.user_id,
            event_type=event.event_type.value,
            amount_in=lp_share,
            amount_out=amount_x + amount_y,
            fee=0.0,
            spot_price=self.pool.spot_price,
            execution_price=None,
            slippage_pct=None,
        )

    def _build_record(
        self,
        *,
        event: Event,
        user_id: str,
        event_type: str,
        direction: str = "",
        amount_in: float | None = None,
        amount_out: float | None = None,
        fee: float | None = None,
        spot_price: float | None = None,
        execution_price: float | None = None,
        slippage_pct: float | None = None,
    ) -> EventRecord:
        return EventRecord(
            event_id=event.event_id,
            timestamp=event.timestamp,
            user_id=user_id,
            event_type=event_type,
            direction=direction,
            amount_in=amount_in,
            amount_out=amount_out,
            fee=fee,
            reserve_x=self.pool.reserve_x,
            reserve_y=self.pool.reserve_y,
            spot_price=spot_price,
            execution_price=execution_price,
            slippage_pct=slippage_pct,
            lp_total_shares=self.pool.total_lp_shares,
        )

    def export_csv(self, path: str | Path) -> Path:
        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = list(EventRecord(0, 0, "", "").to_csv_row().keys())
        with output_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for record in self.records:
                writer.writerow(record.to_csv_row())
        return output_path


def build_events(raw_events: list[dict[str, Any]]) -> list[Event]:
    events: list[Event] = []
    for index, raw_event in enumerate(raw_events, start=1):
        event_type = EventType(raw_event["event_type"])
        payload = {key: value for key, value in raw_event.items() if key not in {"timestamp", "event_type", "user_id"}}
        events.append(
            Event(
                timestamp=float(raw_event.get("timestamp", index)),
                event_id=index,
                event_type=event_type,
                user_id=str(raw_event["user_id"]),
                payload=payload,
            )
        )
    return events
