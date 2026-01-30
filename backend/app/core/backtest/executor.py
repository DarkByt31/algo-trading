from typing import Dict, List, Any, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def calculate_quantity(capital: float, price: float) -> int:
    if price <= 0:
        return 0
    return int(capital // price)


class TradeExecutor:
    """Executes entry and exit operations and records trades."""

    def __init__(self, brokerage_fee: float = 0.0):
        self.brokerage = float(brokerage_fee or 0.0)
        logger.info(f"TradeExecutor initialized with brokerage_fee: {self.brokerage}")

    def enter_long(self, capital: float, price: float) -> Tuple[int, float, float]:
        qty = calculate_quantity(capital, price)
        cost = qty * price + self.brokerage if qty > 0 else 0.0
        capital_after = capital - cost
        logger.debug(f"ENTER_LONG - Capital: {capital}, Price: {price}, Qty: {qty}, Cost: {cost}, Capital_after: {capital_after}")
        return qty, cost, capital_after

    def enter_short(self, capital: float, price: float) -> Tuple[int, float, float]:
        # For short, we assume using full capital as margin to short qty shares at price
        qty = calculate_quantity(capital, price)
        # No immediate cash outflow in simple model; charge brokerage
        cost = self.brokerage if qty > 0 else 0.0
        capital_after = capital - cost
        return -qty, cost, capital_after

    def exit_long(self, capital: float, qty: int, entry_price: float, exit_price: float) -> Tuple[float, float]:
        proceeds = qty * exit_price
        pnl = (exit_price - entry_price) * qty
        capital_after = capital + proceeds - self.brokerage
        logger.debug(f"EXIT_LONG - Capital: {capital}, Qty: {qty}, Entry: {entry_price}, Exit: {exit_price}, PnL: {pnl}, Capital_after: {capital_after}")
        return pnl, capital_after

    def exit_short(self, capital: float, qty: int, entry_price: float, exit_price: float) -> Tuple[float, float]:
        # qty is positive for calculations
        proceeds = qty * (entry_price - exit_price)
        pnl = (entry_price - exit_price) * qty
        capital_after = capital + proceeds - self.brokerage
        return pnl, capital_after

    def record_trade(self, trades: List[Dict[str, Any]], ttype: str, time: datetime, price: float, qty: int, capital: float, extra: Dict[str, Any] = None) -> None:
        rec = {
            'type': ttype,
            'time': time,
            'price': float(price),
            'qty': abs(int(qty)),
            'capital': round(float(capital), 2)
        }
        if extra:
            rec.update(extra)
        trades.append(rec)
