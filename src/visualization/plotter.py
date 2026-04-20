from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from src.simulator.result import SimulationResult


def _save_figure(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=160, bbox_inches="tight")
    plt.close()
    return path


def plot_pool_price(records, output_dir: str | Path) -> Path | None:
    if not records:
        return None

    timestamps = [record.timestamp for record in records]
    spot_prices = [record.spot_price for record in records]

    plt.figure(figsize=(8, 4.5))
    plt.plot(timestamps, spot_prices, color="#0f766e", linewidth=2)
    plt.title("Pool Spot Price")
    plt.xlabel("Timestamp")
    plt.ylabel("Price (Y per X)")
    plt.grid(alpha=0.25)
    return _save_figure(Path(output_dir) / "pool_spot_price.png")


def plot_slippage(records, output_dir: str | Path) -> Path | None:
    swap_records = [record for record in records if record.slippage_pct is not None]
    if not swap_records:
        return None

    timestamps = [record.timestamp for record in swap_records]
    slippage = [record.slippage_pct for record in swap_records]

    plt.figure(figsize=(8, 4.5))
    plt.plot(timestamps, slippage, marker="o", color="#b45309", linewidth=2)
    plt.title("Swap Slippage")
    plt.xlabel("Timestamp")
    plt.ylabel("Slippage (%)")
    plt.grid(alpha=0.25)
    return _save_figure(Path(output_dir) / "swap_slippage.png")


def plot_user_pnl(result: SimulationResult, output_dir: str | Path) -> Path | None:
    pnl_summary = result.summary.user_pnl
    if not pnl_summary:
        return None

    user_ids = list(pnl_summary.keys())
    pnl_values = [pnl_summary[user_id].total_pnl_in_y for user_id in user_ids]
    colors = ["#15803d" if value >= 0 else "#b91c1c" for value in pnl_values]

    plt.figure(figsize=(8, 4.5))
    plt.bar(user_ids, pnl_values, color=colors)
    plt.axhline(0, color="#334155", linewidth=1)
    plt.title("User Total PnL")
    plt.xlabel("User")
    plt.ylabel("PnL (in Y)")
    plt.grid(axis="y", alpha=0.25)
    return _save_figure(Path(output_dir) / "user_total_pnl.png")


def generate_result_plots(result: SimulationResult, output_dir: str | Path) -> dict[str, Path]:
    plots = {
        "pool_spot_price": plot_pool_price(result.records, output_dir),
        "swap_slippage": plot_slippage(result.records, output_dir),
        "user_total_pnl": plot_user_pnl(result, output_dir),
    }
    return {name: path for name, path in plots.items() if path is not None}

