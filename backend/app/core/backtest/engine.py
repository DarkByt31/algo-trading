from typing import Dict, Any, List, Tuple
from datetime import datetime, time
import pandas as pd
import logging
from app.core.algorithms.registry import AlgorithmRegistry
from app.core.backtest.executor import TradeExecutor
from app.core.backtest.validator import ParameterValidator

logger = logging.getLogger(__name__)


class BacktestEngine:
    """Runs backtests given a symbol, algorithm and data."""

    def __init__(self, executor: TradeExecutor):
        self.executor = executor

    def run(self, symbol: str, algorithm_id: str, parameters: Dict[str, Any], df: pd.DataFrame, initial_capital: float, allow_short: bool = True) -> Dict[str, Any]:
        # Validate inputs
        start_date = df['datetime'].min().to_pydatetime()
        end_date = df['datetime'].max().to_pydatetime()
        ParameterValidator.validate_date_range(start_date, end_date)
        ParameterValidator.validate_capital(initial_capital)
        
        logger.info(f"Starting backtest - Symbol: {symbol}, Algorithm: {algorithm_id}, Capital: {initial_capital}, Date Range: {start_date} to {end_date}")
        logger.debug(f"Algorithm Parameters: {parameters}")

        algo = AlgorithmRegistry.get_algorithm(algorithm_id, parameters)
        logger.info(f"Algorithm initialized: {algo.__class__.__name__}")
        
        df_signals = algo.generate_signals(df)
        logger.debug(f"Signals generated for {len(df_signals)} candles")

        capital = float(initial_capital)
        position = 0
        entry_price = 0.0
        trades: List[Dict[str, Any]] = []
        trade_seq = 0
        logger.debug(f"Backtest loop started - Initial Capital: {capital}")

        for i in range(1, len(df_signals)):
            row = df_signals.iloc[i]
            prev = df_signals.iloc[i - 1]
            curr_time = row['datetime'].time()

            # Force exit at or after 15:00
            if position != 0 and curr_time >= time(15, 0):
                # close position at current close
                exit_price = row['close']
                qty = abs(position)
                if position > 0:
                    pnl, capital = self.executor.exit_long(capital, qty, entry_price, exit_price)
                else:
                    pnl, capital = self.executor.exit_short(capital, qty, entry_price, exit_price)

                trade_seq += 1
                logger.info(f"Market Close EXIT at {row['datetime']} - Type: {'LONG' if position > 0 else 'SHORT'}, Price: {exit_price}, PnL: {pnl}")
                self.executor.record_trade(trades, 'EXIT', row['datetime'], exit_price, qty, capital, extra={'pnl': round(float(pnl), 2), 'trade_sequence': trade_seq, 'z_score': float(row.get('z_score', 0)), 'sma': float(row.get('sma', 0))})
                position = 0
                entry_price = 0.0
                continue

            # ENTRY
            if position == 0:
                if prev['signal'] == 'HOLD' and row['signal'] == 'BUY' and capital > 0:
                    qty, cost, capital = self.executor.enter_long(capital, row['close'])
                    if qty == 0:
                        continue
                    position = qty
                    entry_price = row['close']
                    trade_seq += 1
                    logger.info(f"BUY signal at {row['datetime']} - Price: {entry_price}, Qty: {qty}, Z-Score: {row.get('z_score', 0):.4f}")
                    self.executor.record_trade(trades, 'BUY', row['datetime'], entry_price, qty, capital, extra={'trade_sequence': trade_seq, 'z_score': float(row.get('z_score', 0)), 'sma': float(row.get('sma', 0))})

                elif prev['signal'] == 'HOLD' and row['signal'] == 'SELL' and allow_short and capital > 0:
                    qty, cost, capital_after = self.executor.enter_long(capital, row['close'])
                    # Use enter_short semantics
                    qty_short = qty
                    if qty_short == 0:
                        continue
                    position = -qty_short
                    entry_price = row['close']
                    # entering short reduces capital by brokerage only
                    capital = capital_after
                    trade_seq += 1
                    logger.info(f"SELL signal at {row['datetime']} - Price: {entry_price}, Qty: {qty_short}, Z-Score: {row.get('z_score', 0):.4f}")
                    self.executor.record_trade(trades, 'SELL', row['datetime'], entry_price, qty_short, capital, extra={'trade_sequence': trade_seq, 'z_score': float(row.get('z_score', 0)), 'sma': float(row.get('sma', 0))})

            # EXIT based on z-score reverting
            elif position != 0:
                should_exit = False
                z_exit = parameters.get('Z_EXIT_THRESHOLD', 0.3)
                if position > 0 and row['z_score'] > z_exit:
                    should_exit = True
                elif position < 0 and row['z_score'] < -z_exit:
                    should_exit = True

                if should_exit:
                    exit_price = row['close']
                    qty = abs(position)
                    if position > 0:
                        pnl, capital = self.executor.exit_long(capital, qty, entry_price, exit_price)
                    else:
                        pnl, capital = self.executor.exit_short(capital, qty, entry_price, exit_price)

                    trade_seq += 1
                    logger.info(f"Z-Score EXIT at {row['datetime']} - Type: {'LONG' if position > 0 else 'SHORT'}, Price: {exit_price}, PnL: {pnl:.2f}, Z-Score: {row.get('z_score', 0):.4f}")
                    self.executor.record_trade(trades, 'EXIT', row['datetime'], exit_price, qty, capital, extra={'pnl': round(float(pnl), 2), 'trade_sequence': trade_seq, 'z_score': float(row.get('z_score', 0)), 'sma': float(row.get('sma', 0))})
                    position = 0
                    entry_price = 0.0

        # finalize
        result = {
            'symbol': symbol,
            'algorithm_id': algorithm_id,
            'initial_capital': initial_capital,
            'final_capital': round(capital, 2),
            'trades': trades
        }
        total_return = ((capital - initial_capital) / initial_capital * 100) if initial_capital > 0 else 0
        logger.info(f"Backtest completed - Symbol: {symbol}, Total Trades: {len(trades)}, Initial Capital: {initial_capital}, Final Capital: {capital}, Return: {total_return:.2f}%")
        return result
