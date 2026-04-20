from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from src.analytics.report import SimulationSummary


def export_simulation_summary(summary: SimulationSummary, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(asdict(summary), indent=2), encoding="utf-8")
    return output_path

