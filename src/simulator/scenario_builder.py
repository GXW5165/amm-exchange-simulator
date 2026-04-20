from __future__ import annotations

from typing import Any

from .event import Event, EventType


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

