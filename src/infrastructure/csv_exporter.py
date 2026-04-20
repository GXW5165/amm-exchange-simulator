from __future__ import annotations

import csv
from pathlib import Path

from src.analytics.record import EventRecord


def export_event_records(records: list[EventRecord], path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(EventRecord(0, 0, "", "").to_csv_row().keys())
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record.to_csv_row())
    return output_path
