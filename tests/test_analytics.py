from src.analytics.impermanent_loss import impermanent_loss_pct
from src.analytics.pnl import summarize_user_pnl
from src.analytics.slippage import calculate_slippage_pct
from src.domain.pool import Pool
from src.domain.user import User


def test_calculate_slippage_pct_returns_expected_value() -> None:
    slippage = calculate_slippage_pct(2.0, 1.8)
    assert slippage == 10.0


def test_impermanent_loss_pct_is_zero_when_price_unchanged() -> None:
    assert impermanent_loss_pct(1.0, 1.0) == 0.0


def test_summarize_user_pnl_includes_lp_value() -> None:
    initial_users = {"alice": User("alice", balance_x=10.0, balance_y=10.0, lp_shares=0.0)}
    current_users = {"alice": User("alice", balance_x=5.0, balance_y=0.0, lp_shares=10.0)}
    pool = Pool(reserve_x=100.0, reserve_y=100.0, fee_rate=0.003, total_lp_shares=100.0)

    summary = summarize_user_pnl(initial_users, current_users, pool, price_y_per_x=1.0)

    assert summary["alice"].lp_position_value_in_y == 20.0
    assert summary["alice"].final_total_value_in_y == 25.0
    assert summary["alice"].total_pnl_in_y == 5.0
