from pathlib import Path

from src.application.simulation_runner import SimulationRunner
from src.infrastructure.config_loader import load_config


def test_simulation_runner_exports_all_artifacts(tmp_path: Path) -> None:
    config = load_config(Path("configs/default.yaml"))
    config.log_path = "logs/test_simulation.csv"
    config.summary_path = "results/test_summary.json"
    config.plot_dir = "results/plots"

    runner = SimulationRunner(tmp_path)
    artifacts = runner.run_from_config(config)

    assert artifacts.csv_path.exists()
    assert artifacts.summary_path.exists()
    assert artifacts.plot_paths
    assert artifacts.warnings == []
    assert all(path.exists() for path in artifacts.plot_paths.values())
