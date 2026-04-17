from __future__ import annotations

from pathlib import Path

from src.domain.pool import Pool
from src.domain.user import User
from src.infrastructure.config_loader import load_config
from src.infrastructure.logger import get_logger
from src.simulator.engine import SimulatorEngine, build_events


class AMMCLI:
    def __init__(self) -> None:
        self.logger = get_logger()
        self.root_dir = Path(__file__).resolve().parents[2]
        self.config_path = self.root_dir / "configs" / "default.yaml"
        self.pool: Pool | None = None
        self.users: dict[str, User] = {}
        self.engine = SimulatorEngine()
        self._load_default_state()

    def _load_default_state(self) -> None:
        if self.config_path.exists():
            config = load_config(self.config_path)
            self.pool = Pool(config.initial_reserve_x, config.initial_reserve_y, config.fee_rate)
            self.users = config.users
            self.engine = SimulatorEngine(self.pool, self.users)
        else:
            self.pool = Pool(0.0, 0.0)
            self.users = {}
            self.engine = SimulatorEngine(self.pool, self.users)

    def run(self) -> None:
        while True:
            self._print_menu()
            choice = input("请选择操作: ").strip()
            if choice == "1":
                self.run_default_simulation()
            elif choice == "2":
                self.manual_initialize_pool()
            elif choice == "3":
                self.execute_swap()
            elif choice == "4":
                self.add_liquidity()
            elif choice == "5":
                self.remove_liquidity()
            elif choice == "6":
                self.view_pool_status()
            elif choice == "7":
                self.view_user_status()
            elif choice == "8":
                print("已退出")
                break
            else:
                print("无效选择")

    def _print_menu(self) -> None:
        print("\nAMM Exchange Simulator")
        print("1. Use default config to run simulation")
        print("2. Manually initialize pool")
        print("3. Execute a swap")
        print("4. Add liquidity")
        print("5. Remove liquidity")
        print("6. View pool status")
        print("7. View user status")
        print("8. Exit")

    def _require_pool(self) -> Pool:
        if self.pool is None:
            raise RuntimeError("Pool is not initialized")
        return self.pool

    def _get_user(self, user_id: str) -> User:
        if user_id not in self.users:
            self.users[user_id] = User(user_id=user_id)
        return self.users[user_id]

    def run_default_simulation(self) -> None:
        if not self.config_path.exists():
            print("找不到默认配置文件")
            return
        config = load_config(self.config_path)
        self.pool = Pool(config.initial_reserve_x, config.initial_reserve_y, config.fee_rate)
        self.users = config.users
        self.engine = SimulatorEngine(self.pool, self.users)
        events = build_events(config.events)
        result = self.engine.run(events)
        output_path = self.engine.export_csv(self.root_dir / config.log_path)
        print(f"模拟完成，记录数: {len(result.records)}")
        print(f"日志已写入: {output_path}")

    def manual_initialize_pool(self) -> None:
        reserve_x = self._prompt_float("请输入 Token X 初始储备: ")
        reserve_y = self._prompt_float("请输入 Token Y 初始储备: ")
        fee_rate = self._prompt_float("请输入手续费率(例如 0.003): ")
        self.pool = Pool(reserve_x, reserve_y, fee_rate)
        self.engine = SimulatorEngine(self.pool, self.users)
        print("池子已初始化")

    def execute_swap(self) -> None:
        try:
            pool = self._require_pool()
        except RuntimeError as exc:
            print(str(exc))
            return
        user_id = input("user_id: ").strip()
        direction = input("direction(x_to_y / y_to_x): ").strip()
        amount_in = self._prompt_float("amount_in: ")
        event = {
            "timestamp": 0,
            "event_type": "swap",
            "user_id": user_id,
            "direction": direction,
            "amount_in": amount_in,
        }
        try:
            self.engine.process_event(build_events([event])[0])
            print(f"Swap executed. Pool spot price: {pool.spot_price:.6f}")
        except Exception as exc:
            print(f"操作失败: {exc}")

    def add_liquidity(self) -> None:
        try:
            self._require_pool()
        except RuntimeError as exc:
            print(str(exc))
            return
        user_id = input("user_id: ").strip()
        amount_x = self._prompt_float("amount_x: ")
        amount_y = self._prompt_float("amount_y: ")
        event = {
            "timestamp": 0,
            "event_type": "add_liquidity",
            "user_id": user_id,
            "amount_x": amount_x,
            "amount_y": amount_y,
        }
        try:
            self.engine.process_event(build_events([event])[0])
            print("已添加流动性")
        except Exception as exc:
            print(f"操作失败: {exc}")

    def remove_liquidity(self) -> None:
        try:
            self._require_pool()
        except RuntimeError as exc:
            print(str(exc))
            return
        user_id = input("user_id: ").strip()
        lp_share = self._prompt_float("lp_share: ")
        event = {
            "timestamp": 0,
            "event_type": "remove_liquidity",
            "user_id": user_id,
            "lp_share": lp_share,
        }
        try:
            self.engine.process_event(build_events([event])[0])
            print("已移除流动性")
        except Exception as exc:
            print(f"操作失败: {exc}")

    def view_pool_status(self) -> None:
        try:
            pool = self._require_pool()
        except RuntimeError as exc:
            print(str(exc))
            return
        print(f"reserve_x: {pool.reserve_x:.6f}")
        print(f"reserve_y: {pool.reserve_y:.6f}")
        print(f"fee_rate: {pool.fee_rate:.6f}")
        print(f"spot_price(y per x): {pool.spot_price:.6f}")
        print(f"lp_total_shares: {pool.total_lp_shares:.6f}")

    def view_user_status(self) -> None:
        if not self.users:
            print("暂无用户")
            return
        for user in self.users.values():
            print(
                f"{user.user_id}: balance_x={user.balance_x:.6f}, balance_y={user.balance_y:.6f}, lp_shares={user.lp_shares:.6f}"
            )

    def _prompt_float(self, prompt: str) -> float:
        while True:
            try:
                return float(input(prompt).strip())
            except ValueError:
                print("请输入有效数字")


def main() -> None:
    AMMCLI().run()
