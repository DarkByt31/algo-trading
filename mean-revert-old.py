import pandas as pd
import numpy as np
import datetime
from kiteconnect import KiteConnect
import matplotlib.pyplot as plt
import time

# === CONFIG ===
API_KEY = "8kb1ag60chrc88ol"
API_SECRET = "26y0pw6mdwkurjn6e2z01hqtxti942zj"
ACCESS_TOKEN = "5iTJZ0RTLyGKLIqJ0qCngkal1g3R3P6c"

STOCK_LIST = ["RELIANCE", "VOLTAS", "TATVA"]
EXCHANGE = "NSE"
INTERVAL = "5minute"
LOOKBACK_DAYS = 14
SMA_WINDOW = 20
Z_ENTRY = 1
CAPITAL = 50000

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
    df['datetime'] = pd.to_datetime(df['date'])
    df = df[['datetime', 'close']]
    return df

# === Mean Reversion Logic ===
def apply_mean_reversion(df):
    df['sma'] = df['close'].rolling(SMA_WINDOW).mean()
    df['std'] = df['close'].rolling(SMA_WINDOW).std()
    df['z_score'] = (df['close'] - df['sma']) / df['std']
    df['signal'] = np.where(df['z_score'] < -Z_ENTRY, 'BUY',
                    np.where(df['z_score'] > Z_ENTRY, 'SELL', 'HOLD'))
    df['position'] = df['signal'].shift().fillna('HOLD')
    return df.dropna()

# === Backtest Logic ===
def backtest(symbol, df):
    capital = CAPITAL
    position = 0
    entry_price = 0
    trades = []

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i - 1]

        # ENTER position only if FLAT
        if position == 0:
            if prev['signal'] == 'HOLD' and row['signal'] == 'BUY' and capital > 0:
                entry_price = row['close']
                qty = int(capital / entry_price)
                if qty == 0:
                    continue
                position = qty
                capital -= qty * entry_price
                trades.append({
                    'type': 'BUY',
                    'time': row['datetime'],
                    'price': entry_price,
                    'qty': qty,
                    'capital': round(capital, 2)
                })

            elif prev['signal'] == 'HOLD' and row['signal'] == 'SELL' and capital > 0:
                entry_price = row['close']
                qty = int(capital / entry_price)
                if qty == 0:
                    continue
                position = -qty
                trades.append({
                    'type': 'SELL',
                    'time': row['datetime'],
                    'price': entry_price,
                    'qty': qty,
                    'capital': round(capital, 2)
                })

        # EXIT only if a position is active and signal has reverted to HOLD
        elif position != 0 and row['signal'] == 'HOLD':
            exit_price = row['close']
            qty = abs(position)
            if position > 0:  # closing BUY
                capital += qty * exit_price
            else:  # closing SELL
                capital += qty * (entry_price - exit_price)
            trades.append({
                'type': 'EXIT',
                'time': row['datetime'],
                'price': exit_price,
                'qty': qty,
                'capital': round(capital, 2)
            })
            position = 0


    final_value = capital
    print(f"\n[{symbol}]")
    print(f"Net Capital After Backtest: ₹{round(final_value, 2)}")
    print(f"Net Profit: ₹{round(final_value - CAPITAL, 2)}")

    # Print trade log
    print("\nExecuted Trades:")
    for t in trades:
        print(f"{t['time']} - {t['type']} - Qty: {t['qty']} @ ₹{t['price']} | Capital: ₹{round(t['capital'], 2)}")

    # Plot strategy returns
    df['returns'] = df['close'].pct_change()
    df['strategy_returns'] = df['returns'] * np.where(df['position'] == 'BUY', 1,
                                                      np.where(df['position'] == 'SELL', -1, 0))
    df['cumulative_returns'] = (1 + df['strategy_returns']).cumprod()

    plt.figure(figsize=(10, 4))
    plt.plot(df['datetime'], df['cumulative_returns'], label="Strategy Returns")
    plt.title(f"{symbol} - Mean Reversion Backtest")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Returns")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    #plt.show()


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