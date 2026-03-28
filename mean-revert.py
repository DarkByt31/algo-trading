import pandas as pd
import numpy as np
import datetime
from kiteconnect import KiteConnect
import matplotlib.pyplot as plt
import time
import pytz

# === CONFIG ===
API_KEY = "8kb1ag60chrc88ol"
API_SECRET = "26y0pw6mdwkurjn6e2z01hqtxti942zj"
ACCESS_TOKEN = "j5d4V1ifvzDd6oQQ9qw1eBIAqFEnqfeK"

STOCK_LIST = ["RELIANCE", "VOLTAS", "TATVA"]
EXCHANGE = "NSE"
INTERVAL = "5minute"
LOOKBACK_DAYS = 14
SMA_WINDOW = 20
Z_ENTRY = 1
CAPITAL = 50000
MAX_TRADE_CAPITAL = 10000
IST = pytz.timezone('Asia/Kolkata')

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

# === Fetch Instrument Token ===
def get_token(symbol):
    instruments = kite.instruments(EXCHANGE)
    for i in instruments:
        if i['tradingsymbol'] == symbol:
            return i['instrument_token']
    raise Exception(f"Token not found for {symbol}")

# === Fetch Intraday Data ===
def fetch_data(symbol):
    token = get_token(symbol)
    to_date = datetime.datetime.now()
    from_date = to_date - datetime.timedelta(days=LOOKBACK_DAYS)
    data = kite.historical_data(token, from_date, to_date, INTERVAL)
    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['date']).dt.tz_convert(IST)
    df = df[['datetime', 'close']]
    return df

# === Mean Reversion Logic ===
def apply_mean_reversion(df):
    df['sma'] = df['close'].rolling(SMA_WINDOW).mean()
    df['std'] = df['close'].rolling(SMA_WINDOW).std()
    df['z_score'] = (df['close'] - df['sma']) / df['std']
    df['signal'] = np.where(df['z_score'] < -Z_ENTRY, 'BUY',
                    np.where(df['z_score'] > Z_ENTRY, 'SELL', 'HOLD'))
    return df.dropna()

# === Backtest Logic with Multiple Positions ===
def backtest(symbol, df):
    capital = CAPITAL
    open_positions = []  # List of dicts: type, entry_price, qty, time
    trades = []

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]
        time_now = row['datetime'].time()

        # Entry logic
        if prev['signal'] == 'HOLD' and row['signal'] in ['BUY', 'SELL']:
            if capital >= 1000:  # Ensure we have enough to take a trade
                entry_price = row['close']
                allowed_cap = min(MAX_TRADE_CAPITAL, capital)
                qty = int(allowed_cap / entry_price)
                if qty > 0:
                    capital -= qty * entry_price
                    open_positions.append({
                        'type': row['signal'],
                        'entry_price': entry_price,
                        'qty': qty,
                        'entry_time': row['datetime']
                    })
                    trades.append({
                        'type': row['signal'],
                        'time': row['datetime'],
                        'price': entry_price,
                        'qty': qty,
                        'capital': round(capital, 2)
                    })

        # Exit logic if signal reverts or end-of-day
        exit_due_to_signal = (row['signal'] == 'HOLD')
        exit_due_to_time = (time_now >= datetime.time(15, 0))  # Close all by 3:00 PM

        if exit_due_to_signal or exit_due_to_time:
            exited = []
            for pos in open_positions:
                exit_price = row['close']
                pnl = pos['qty'] * exit_price
                capital += pnl
                trades.append({
                    'type': 'EXIT',
                    'time': row['datetime'],
                    'price': exit_price,
                    'qty': pos['qty'],
                    'capital': round(capital, 2)
                })
                exited.append(pos)
            for pos in exited:
                open_positions.remove(pos)

    final_value = capital
    print(f"\n[{symbol}]")
    print(f"Net Capital After Backtest: ₹{round(final_value, 2)}")
    print(f"Net Profit: ₹{round(final_value - CAPITAL, 2)}")

    # Print trade log
    print("\nExecuted Trades:")
    for t in trades:
        print(f"{t['time']} - {t['type']} - Qty: {t['qty']} @ ₹{t['price']} | Capital: ₹{round(t['capital'], 2)}")

    # Strategy returns (approximate cumulative logic)
    df['returns'] = df['close'].pct_change()
    df['strategy_returns'] = df['returns'] * np.where(df['signal'].shift() == 'BUY', 1,
                                                      np.where(df['signal'].shift() == 'SELL', -1, 0))
    df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()

    plt.figure(figsize=(10, 4))
    plt.plot(df['datetime'], df['cumulative_returns'], label="Strategy Returns")
    plt.title(f"{symbol} - Mean Reversion Backtest")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Returns")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# === Main Execution ===
if __name__ == "__main__":
    for symbol in STOCK_LIST:
        try:
            print(f"\nProcessing {symbol}...")
            df = fetch_data(symbol)
            df = apply_mean_reversion(df)
            backtest(symbol, df)
            time.sleep(2)
        except Exception as e:
            print(f"Error with {symbol}: {e}")