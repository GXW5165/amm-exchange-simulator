from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EventType(str, Enum):
    SWAP = "swap"
    ADD_LIQUIDITY = "add_liquidity"
    REMOVE_LIQUIDITY = "remove_liquidity"


@dataclass(order=True)
class Event:
    timestamp: float
    event_id: int = field(compare=False)
    event_type: EventType = field(compare=False)
    user_id: str = field(compare=False)
    payload: dict[str, Any] = field(compare=False, default_factory=dict)
