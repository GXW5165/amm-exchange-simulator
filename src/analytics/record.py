from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class EventRecord:
    event_id: int
    timestamp: float
    user_id: str
    event_type: str
    direction: str = ""
    amount_in: Optional[float] = None
    amount_out: Optional[float] = None
    fee: Optional[float] = None
    reserve_x: float = 0.0
    reserve_y: float = 0.0
    spot_price: Optional[float] = None
    execution_price: Optional[float] = None
    slippage_pct: Optional[float] = None
    lp_total_shares: float = 0.0

    def to_csv_row(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "event_type": self.event_type,
            "direction": self.direction,
            "amount_in": self.amount_in,
            "amount_out": self.amount_out,
            "fee": self.fee,
            "reserve_x": self.reserve_x,
            "reserve_y": self.reserve_y,
            "spot_price": self.spot_price,
            "execution_price": self.execution_price,
            "slippage_pct": self.slippage_pct,
            "lp_total_shares": self.lp_total_shares,
        }

