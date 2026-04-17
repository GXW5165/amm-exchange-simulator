from __future__ import annotations

import heapq
from itertools import count
from typing import Optional

from .event import Event


class EventQueue:
    def __init__(self) -> None:
        self._heap: list[tuple[float, int, Event]] = []
        self._sequence = count()

    def push(self, event: Event) -> None:
        heapq.heappush(self._heap, (event.timestamp, next(self._sequence), event))

    def pop(self) -> Optional[Event]:
        if not self._heap:
            return None
        _, _, event = heapq.heappop(self._heap)
        return event

    def extend(self, events: list[Event]) -> None:
        for event in events:
            self.push(event)

    def empty(self) -> bool:
        return not self._heap
