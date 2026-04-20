from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass

from src.analytics.record import EventRecord
from src.analytics.report import SimulationSummary, summarize_records
from src.domain.pool import Pool
from src.domain.user import User


@dataclass
class SimulationResult:
    records: list[EventRecord]
    pool: Pool
    users: dict[str, User]
    initial_pool: Pool
    initial_users: dict[str, User]

    @property
    def summary(self) -> SimulationSummary:
        return summarize_records(
            records=self.records,
            initial_pool=deepcopy(self.initial_pool),
            current_pool=deepcopy(self.pool),
            initial_users=deepcopy(self.initial_users),
            current_users=deepcopy(self.users),
        )
