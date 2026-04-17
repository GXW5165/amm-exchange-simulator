from dataclasses import dataclass


@dataclass
class LPPosition:
    user_id: str
    shares: float
    amount_x: float
    amount_y: float
