import pandas as pd
import numpy as np
import datetime
from kiteconnect import KiteConnect
import time
import json
from scipy.signal import argrelextrema
from log_and_plot_utils import print_trade_log, plot_mean_reversion_signals, plot_weekly_gains

# === CONFIG ===
CONFIG_PATH = "kite_config.json"
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

API_KEY = config["api_key"]
API_SECRET = config["api_secret"]
ACCESS_TOKEN = config["access_token"]


STOCK_LIST = ["RELIANCE"] #, "VOLTAS", "TATVA"]
EXCHANGE = "NSE"
INTERVAL = "5minute"
LOOKBACK_DAYS = 30
SMA_WINDOW = 20
Z_ENTRY = 1
Z_EXIT_THRESHOLD = 0.3
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

    # Keep only NSE market hours
    df = df[(df['datetime'].dt.time >= datetime.time(9, 15)) & 
            (df['datetime'].dt.time <= datetime.time(15, 30))]

    df = df[['datetime', 'close']]
    return df

# === Mean Reversion Logic ===
def apply_mean_reversion(df):
    df['sma'] = df['close'].rolling(SMA_WINDOW).mean()
    df['std'] = df['close'].rolling(SMA_WINDOW).std()
    df['z_score'] = (df['close'] - df['sma']) / df['std']
    df['signal'] = 'HOLD'

    for i in range(2, len(df)):
        z_prev2 = df.loc[i - 2, 'z_score']
        z_prev1 = df.loc[i - 1, 'z_score']
        z_curr = df.loc[i, 'z_score']

        # Detect local max (SELL)
        if z_prev2 < z_prev1 > z_curr and z_curr > Z_ENTRY:
            df.loc[i, 'signal'] = 'SELL'

        # Detect local min (BUY)
        elif z_prev2 > z_prev1 < z_curr and z_curr < -Z_ENTRY:
            df.loc[i, 'signal'] = 'BUY'

    # Shift signal to avoid forward bias in execution
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

        # EXIT when Z-score reverts toward mean
        elif position != 0:
            should_exit = False
            if position > 0 and row['z_score'] > Z_EXIT_THRESHOLD:
                should_exit = True
            elif position < 0 and row['z_score'] < -Z_EXIT_THRESHOLD:
                should_exit = True

            if should_exit:
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
    print_trade_log(symbol, trades, final_value, CAPITAL)
    plot_mean_reversion_signals(symbol, df, trades, Z_ENTRY)
    plot_weekly_gains(trades, CAPITAL)


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