# AMM Exchange Simulator (Offline MVP)

## 1. Project Overview
This project is a minimal, offline Automated Market Maker (AMM) simulator for a single token pair (Token X / Token Y). It implements the constant product model `x * y = k`, supports swaps, liquidity provision/removal, slippage, fees, and a simple discrete-event simulation engine. The system is fully local and runs on Python 3.10+.

## 2. Directory Structure
```
amm_exchange_simulator/
├── main.py
├── requirements.txt
├── README.md
├── configs/
│   └── default.yaml
├── data/
│   └── output/
│       └── logs/
├── src/
│   ├── domain/
│   │   ├── pool.py
│   │   ├── user.py
│   │   ├── lp_position.py
│   │   ├── metrics.py
│   │   └── exceptions.py
│   ├── simulator/
│   │   ├── event.py
│   │   ├── event_queue.py
│   │   └── engine.py
│   ├── infrastructure/
│   │   ├── config_loader.py
│   │   └── logger.py
│   └── interface/
│       └── cli.py
└── tests/
    ├── test_pool.py
    ├── test_liquidity.py
    └── test_simulator.py
```

## 3. Environment Setup
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## 4. How to Run
```bash
python main.py
```

## 5. CLI Usage
Menu options:
1. Use default config to run simulation
2. Manually initialize pool
3. Execute a swap
4. Add liquidity
5. Remove liquidity
6. View pool status
7. View user status
8. Exit

## 6. YAML Config Notes
`configs/default.yaml` contains:
- `initial_reserve_x`, `initial_reserve_y`: initial pool reserves
- `fee_rate`: default 0.003
- `seed`: deterministic seed placeholder
- `users`: user balances
- `events`: discrete events list
- `log_path`: output CSV path

Event payloads:
- swap: `user_id`, `direction` (`x_to_y` or `y_to_x`), `amount_in`
- add_liquidity: `user_id`, `amount_x`, `amount_y`
- remove_liquidity: `user_id`, `lp_share`

## 7. Output Example
Simulation writes CSV logs with fields:
`event_id, timestamp, user_id, event_type, direction, amount_in, amount_out, fee, reserve_x, reserve_y, spot_price, execution_price, slippage_pct, lp_total_shares`

Execution price is defined as `y per x`. For `x_to_y`, `execution_price = amount_out / amount_in`. For `y_to_x`, `execution_price = amount_in / amount_out`. Slippage is computed against the spot price `reserve_y / reserve_x`.

## 8. Future Extensions (Not Implemented in P0)
- P1: multi-asset pools, arbitrageur, backtesting, visualization
- P2: concentrated liquidity (Uniswap V3), advanced reporting, concurrency

This MVP focuses strictly on P0 features only.
