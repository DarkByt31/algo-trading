from typing import List, Dict, Any
import numpy as np


class PerformanceCalculator:
    """Compute basic performance metrics from trades and capital series."""

    @staticmethod
    def compute_trade_metrics(trades: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'best_trade_pnl': 0.0,
                'worst_trade_pnl': 0.0,
                'profit_factor': 0.0,
                'avg_trade_pnl': 0.0
            }

        # extract exit trades with pnl
        pnls = [t.get('pnl') for t in trades if t.get('type') == 'EXIT' and t.get('pnl') is not None]
        pnls = [float(x) for x in pnls]
        total_trades = len(pnls)
        winning = [p for p in pnls if p > 0]
        losing = [p for p in pnls if p <= 0]

        win_count = len(winning)
        lose_count = len(losing)
        win_rate = (win_count / total_trades * 100) if total_trades > 0 else 0.0
        best = max(pnls) if pnls else 0.0
        worst = min(pnls) if pnls else 0.0

        gross_profit = sum([p for p in pnls if p > 0])
        gross_loss = -sum([p for p in pnls if p < 0])
        profit_factor = (gross_profit / gross_loss) if gross_loss != 0 else float('inf') if gross_profit>0 else 0.0

        avg_pnl = np.mean(pnls) if pnls else 0.0

        return {
            'total_trades': total_trades,
            'winning_trades': win_count,
            'losing_trades': lose_count,
            'win_rate': round(win_rate, 2),
            'best_trade_pnl': round(best, 2),
            'worst_trade_pnl': round(worst, 2),
            'profit_factor': round(profit_factor, 2) if isinstance(profit_factor, float) and profit_factor!=float('inf') else profit_factor,
            'avg_trade_pnl': round(avg_pnl, 2)
        }
