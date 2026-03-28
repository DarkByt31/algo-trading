import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.data.fetcher import MockDataFetcher
from app.core.data.cache import get_cache
from app.core.algorithms.registry import AlgorithmRegistry
from app.core.backtest.executor import TradeExecutor
from app.core.backtest.engine import BacktestEngine
from app.core.backtest.calculator import PerformanceCalculator


def test_end_to_end_backtest(algorithm_params):
    fetcher = MockDataFetcher()
    from_date = fetcher.fetch_historical_data.__defaults__ if hasattr(fetcher.fetch_historical_data, '__defaults__') else None
    # Use explicit dates
    from datetime import datetime
    df = fetcher.fetch_historical_data('RELIANCE', datetime(2026,1,1), datetime(2026,1,5))

    algo = AlgorithmRegistry.get_algorithm('mean_reversion', algorithm_params)
    df_signals = algo.generate_signals(df)

    executor = TradeExecutor(brokerage_fee=20)
    engine = BacktestEngine(executor)

    result = engine.run('RELIANCE', 'mean_reversion', algorithm_params, df, initial_capital=50000, allow_short=True)

    assert 'final_capital' in result
    assert 'trades' in result

    # Compute metrics
    metrics = PerformanceCalculator.compute_trade_metrics(result['trades'])
    assert 'total_trades' in metrics
    assert metrics['total_trades'] >= 0
