from src.domain.pool import Pool


def test_swap_x_to_y_updates_reserves() -> None:
    pool = Pool(1000.0, 1000.0, 0.003)
    amount_out, fee = pool.swap("x_to_y", 10.0)

    assert fee == 0.03
    assert amount_out > 0
    assert pool.reserve_x > 1000.0
    assert pool.reserve_y < 1000.0


def test_add_and_remove_liquidity() -> None:
    pool = Pool(1000.0, 1000.0, 0.003)
    consumed_x, consumed_y, minted_shares = pool.add_liquidity(100.0, 100.0)

    assert consumed_x == 100.0
    assert consumed_y == 100.0
    assert minted_shares > 0

    amount_x, amount_y = pool.remove_liquidity(minted_shares)
    assert amount_x > 0
    assert amount_y > 0
