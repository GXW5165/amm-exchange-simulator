from pathlib import Path

from src.infrastructure.config_loader import load_config
from src.simulator.engine import SimulatorEngine, build_events


def test_default_config_can_be_loaded_and_run() -> None:
    config = load_config(Path("configs/default.yaml"))
    pool = __import__("src.domain.pool", fromlist=["Pool"]).Pool(
        config.initial_reserve_x,
        config.initial_reserve_y,
        config.fee_rate,
    )
    engine = SimulatorEngine(pool, config.users)
    result = engine.run(build_events(config.events))

    assert len(result.records) == len(config.events)
    assert result.pool.total_lp_shares >= 0
