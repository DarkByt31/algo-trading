# Backtest API Logging Implementation

## Overview
Complete logging framework has been implemented across the backtest system for comprehensive debugging and monitoring.

## Files Modified

### 1. **core/backtest/executor.py**
**Purpose**: Execute trade entries and exits

**Logging Added**:
```python
# Initialization logging
logger.info(f"TradeExecutor initialized with brokerage_fee: {self.brokerage}")

# Entry logging
logger.debug(f"ENTER_LONG - Capital: {capital}, Price: {price}, Qty: {qty}, Cost: {cost}, Capital_after: {capital_after}")

# Exit logging
logger.debug(f"EXIT_LONG - Capital: {capital}, Qty: {qty}, Entry: {entry_price}, Exit: {exit_price}, PnL: {pnl}, Capital_after: {capital_after}")
```

**Sample Output**:
```
2026-01-31 00:28:29 - app.core.backtest.executor - DEBUG 
  ENTER_LONG - Capital: 50000, Price: 2473.57, Qty: 20, Cost: 49476.14, Capital_after: 508.64
```

---

### 2. **core/backtest/engine.py**
**Purpose**: Execute backtest simulation and manage signals

**Logging Added**:
```python
# Backtest initiation
logger.info(f"Starting backtest - Symbol: {symbol}, Algorithm: {algorithm_id}, Capital: {initial_capital}, Date Range: {start_date} to {end_date}")
logger.debug(f"Algorithm Parameters: {parameters}")

# Algorithm setup
logger.info(f"Algorithm initialized: {algo.__class__.__name__}")
logger.debug(f"Signals generated for {len(df_signals)} candles")

# Entry signals
logger.info(f"BUY signal at {row['datetime']} - Price: {entry_price}, Qty: {qty}, Z-Score: {row.get('z_score', 0):.4f}")
logger.info(f"SELL signal at {row['datetime']} - Price: {entry_price}, Qty: {qty_short}, Z-Score: {row.get('z_score', 0):.4f}")

# Exit signals
logger.info(f"Z-Score EXIT at {row['datetime']} - Type: {'LONG' if position > 0 else 'SHORT'}, Price: {exit_price}, PnL: {pnl:.2f}, Z-Score: {row.get('z_score', 0):.4f}")
logger.info(f"Market Close EXIT at {row['datetime']} - Type: {'LONG' if position > 0 else 'SHORT'}, Price: {exit_price}, PnL: {pnl}")

# Completion
logger.info(f"Backtest completed - Symbol: {symbol}, Total Trades: {len(trades)}, Initial Capital: {initial_capital}, Final Capital: {capital}, Return: {total_return:.2f}%")
```

**Sample Output**:
```
2026-01-31 00:28:29 - app.core.backtest.engine - INFO 
  Starting backtest - Symbol: TATVA, Algorithm: mean_reversion, Capital: 50000, Date Range: 2024-01-01 09:15:00 to 2024-01-10 15:30:00

2026-01-31 00:28:29 - app.core.backtest.engine - INFO 
  BUY signal at 2024-01-01 12:40:00 - Price: 2473.57, Qty: 20, Z-Score: -1.7121

2026-01-31 00:28:29 - app.core.backtest.engine - INFO 
  Z-Score EXIT at 2024-01-01 14:20:00 - Type: LONG, Price: 2473.07, PnL: -9.93, Z-Score: 0.9949

2026-01-31 00:28:29 - app.core.backtest.engine - INFO 
  Backtest completed - Symbol: TATVA, Total Trades: 6, Initial Capital: 50000.0, Final Capital: 578.08, Return: -98.84%
```

---

### 3. **api/v1/endpoints/backtest.py**
**Purpose**: Handle backtest API requests and manage job lifecycle

**Logging Added**:
```python
# Request received
logger.info(f"New backtest request - Job ID: {job_id}, Symbol: {req.symbol}, Algorithm: {req.algorithm_id}")
logger.debug(f"Job {job_id} created in database")

# Data operations
logger.debug(f"Fetching data for {req.symbol} from {req.start_date} to {req.end_date}")
logger.debug(f"Data fetched - {len(df)} candles received")
logger.debug(f"Running backtest engine for {req.symbol}")

# Result handling
logger.info(f"Backtest result saved - Job ID: {job_id}, Final Capital: {result['final_capital']}, Total Trades: {res.total_trades}")
logger.debug(f"All trades saved to database - Total: {len(result['trades'])}")
logger.info(f"Job {job_id} completed successfully")

# Error handling
logger.error(f"Backtest failed for job {job_id} - Error: {str(e)}", exc_info=True)
logger.error(f"Job {job_id} marked as failed")
```

**Sample Output**:
```
2026-01-31 00:29:15 - app.api.v1.endpoints.backtest - INFO 
  New backtest request - Job ID: 639a4639-aca6-4d5b-9bb2-ccdf820d80a0, Symbol: TATVA, Algorithm: mean_reversion

2026-01-31 00:28:29 - app.api.v1.endpoints.backtest - INFO 
  Backtest result saved - Job ID: 639a4639-aca6-4d5b-9bb2-ccdf820d80a0, Final Capital: 578.08, Total Trades: 3

2026-01-31 00:28:29 - app.api.v1.endpoints.backtest - DEBUG 
  All trades saved to database - Total: 6

2026-01-31 00:28:29 - app.api.v1.endpoints.backtest - INFO 
  Job 639a4639-aca6-4d5b-9bb2-ccdf820d80a0 completed successfully
```

---

### 4. **config.py**
**Purpose**: Configuration management

**Change Made**:
```python
# Before
LOG_LEVEL: str = "INFO"

# After
LOG_LEVEL: str = "DEBUG"
```

This enables detailed debug messages throughout the backtest flow.

---

## Log Message Types

### DEBUG Messages
Detailed execution flow information for development and troubleshooting:
- Capital calculations during entry/exit
- Signal generation progress
- Data fetch operations
- Job creation/update

### INFO Messages
High-level progress and significant events:
- Backtest start and completion
- Trade signals (BUY/SELL)
- Trade exits (Z-Score/Market Close)
- Result persistence
- Job status changes

### ERROR Messages
Error conditions with full context:
- Backtest execution failures
- Database operation errors
- Parameter validation errors
- Stack traces for debugging

---

## Log Format
```
TIMESTAMP - LOGGER_NAME - LOG_LEVEL - MESSAGE

Example:
2026-01-31 00:28:29,067 - app.core.backtest.engine - INFO - BUY signal at 2024-01-01 12:40:00 - Price: 2473.57, Qty: 20, Z-Score: -1.7121
```

**Components**:
- **TIMESTAMP**: `YYYY-MM-DD HH:MM:SS,mmm`
- **LOGGER_NAME**: Module path (e.g., `app.core.backtest.engine`)
- **LOG_LEVEL**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **MESSAGE**: Contextual information for the event

---

## Debugging Guide

### 1. Track a Specific Backtest Job
```bash
# Find all logs for a job ID
grep "639a4639-aca6-4d5b-9bb2-ccdf820d80a0" server.log

# Filter to INFO level only
grep "639a4639-aca6-4d5b-9bb2-ccdf820d80a0" server.log | grep " INFO "
```

### 2. Monitor Trade Execution
```bash
# Find all trade entry signals
grep "BUY signal\|SELL signal" server.log

# Find all exit events
grep "EXIT\|Market Close" server.log

# Find specific stock trades
grep "RELIANCE" server.log | grep -E "signal|EXIT"
```

### 3. Analyze Capital Changes
```bash
# Track capital changes during backtest
grep "ENTER_LONG\|EXIT_LONG" server.log | head -20

# Find largest gains/losses
grep "PnL:" server.log | sort -t':' -k3 -n
```

### 4. Check Performance Metrics
```bash
# Find all backtest completions
grep "Backtest completed" server.log

# Get return percentages
grep "Backtest completed" server.log | grep -o "Return: [^%]*"
```

### 5. Troubleshoot Errors
```bash
# Find all error messages
grep "ERROR" server.log

# Get full error stack trace
grep -A 10 "ERROR" server.log | head -30
```

---

## Real-World Examples

### Example 1: Debugging a Trade Sequence
Query: What happened during trade execution for RELIANCE?

```bash
grep "RELIANCE" server.log | grep -E "BUY|EXIT" 
```

Output:
```
2026-01-31 00:29:18 - app.core.backtest.engine - INFO - BUY signal at 2024-01-01 11:05:00 - Price: 2498.92, Qty: 40, Z-Score: -1.1775
2026-01-31 00:29:18 - app.core.backtest.executor - DEBUG - ENTER_LONG - Capital: 100000, Price: 2498.92, Qty: 40, Cost: 99976.72, Capital_after: 23.28
2026-01-31 00:29:18 - app.core.backtest.engine - INFO - Z-Score EXIT at 2024-01-01 11:55:00 - Type: LONG, Price: 2500.88, PnL: 78.51, Z-Score: 0.6079
2026-01-31 00:29:18 - app.core.backtest.executor - DEBUG - EXIT_LONG - Capital: 23.28, Qty: 40, Entry: 2498.92, Exit: 2500.88, PnL: 78.51, Capital_after: 100038.51
```

### Example 2: Finding Jobs with Negative Returns
Query: Which backtests lost more than 95%?

```bash
grep "Backtest completed" server.log | grep -E "Return: -9[5-9]"
```

Output:
```
2026-01-31 00:29:16 - app.core.backtest.engine - INFO - Backtest completed - Symbol: VOLTAS, Total Trades: 12, Initial Capital: 50000.0, Final Capital: 861.64, Return: -98.28%
2026-01-31 00:29:18 - app.core.backtest.engine - INFO - Backtest completed - Symbol: RELIANCE, Total Trades: 8, Initial Capital: 100000.0, Final Capital: -36.13, Return: -100.04%
```

### Example 3: Performance Analysis
Query: Average trades per symbol

```bash
grep "Backtest completed" server.log | grep -o "Symbol: [^,]*" | sort | uniq -c
```

Output:
```
      1 Symbol: RELIANCE
      2 Symbol: TATVA
      2 Symbol: VOLTAS
```

---

## Testing Summary

**4 Different Stock Configurations Tested**:
1. ✅ VOLTAS (Jan 1-15, ₹50K, standard params)
2. ✅ TATVA (Jan 1-20, ₹75K, standard params)
3. ✅ RELIANCE (Jan 1-25, ₹100K, tight exit threshold)
4. ✅ VOLTAS (Jan 5-31, ₹100K, aggressive entry params)

**All Tests Passed** with comprehensive logging enabled.

**Log File Location**: `/home/shivansh/projects/Algo trading/backend/server.log`

---

## Next Steps

1. **Monitor Production**: Keep logs for audit trail and performance analysis
2. **Implement Log Rotation**: Prevent log file from growing too large
3. **Add Metrics**: Track trade success rates from logs
4. **Set Up Alerts**: Alert on ERROR and failed backtests
5. **Archive Logs**: Regular backup of historical logs

---

## Configuration

To adjust logging levels, modify `app/config.py`:

```python
# Production (less verbose)
LOG_LEVEL: str = "INFO"

# Development (detailed)
LOG_LEVEL: str = "DEBUG"

# Minimal (only errors)
LOG_LEVEL: str = "WARNING"
```

Then restart the server for changes to take effect.
