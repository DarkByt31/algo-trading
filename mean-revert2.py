import pandas as pd
import numpy as np
import datetime
from kiteconnect import KiteConnect
import matplotlib.pyplot as plt
import time
import json
from scipy.signal import argrelextrema

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
LOOKBACK_DAYS = 4
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
            if position > 0 and row['z_score'] > -Z_EXIT_THRESHOLD:
                should_exit = True
            elif position < 0 and row['z_score'] < Z_EXIT_THRESHOLD:
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
    print(f"\n[{symbol}]")
    print(f"Net Capital After Backtest: ₹{round(final_value, 2)}")
    print(f"Net Profit: ₹{round(final_value - CAPITAL, 2)}")

    # Print trade log
    print(f"\nExecuted Trades: {len(trades) / 2}")
    for t in trades:
        print(f"{t['time']} - {t['type']} - Qty: {t['qty']} @ ₹{t['price']} | Capital: ₹{round(t['capital'], 2)}")

    # Plot strategy returns
    plot_mean_reversion_signals(symbol, df, trades)

def plot_mean_reversion_signals(symbol, df, trades):
    df = df.reset_index(drop=True)
    df['time_index'] = df.index

    buy_signals = df[df['signal'] == 'BUY']
    sell_signals = df[df['signal'] == 'SELL']
    exit_times = [t['time'] for t in trades if t['type'] == 'EXIT']
    exit_df = df[df['datetime'].isin(exit_times)]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # Price and signals
    ax1.plot(df['time_index'], df['close'], label='Close Price', color='blue', alpha=0.7)
    ax1.plot(df['time_index'], df['sma'], label='SMA', color='orange', linestyle='--')
    ax1.scatter(buy_signals['time_index'], buy_signals['close'], label='Buy Signal', marker='^', color='green')
    ax1.scatter(sell_signals['time_index'], sell_signals['close'], label='Sell Signal', marker='v', color='red')
    ax1.scatter(exit_df['time_index'], exit_df['close'], label='Exit', marker='x', color='black')
    ax1.set_ylabel('Price')
    ax1.set_title(f'{symbol} - Price and Mean Reversion Signals')
    ax1.legend()
    ax1.grid(True)

    # Z-score plot
    ax2.plot(df['time_index'], df['z_score'], label='Z-Score', color='purple')
    ax2.axhline(Z_ENTRY, color='red', linestyle='--', label=f'+Z_ENTRY ({Z_ENTRY})')
    ax2.axhline(-Z_ENTRY, color='green', linestyle='--', label=f'-Z_ENTRY ({-Z_ENTRY})')
    ax2.axhline(0, color='black', linestyle=':')
    ax2.scatter(buy_signals['time_index'], buy_signals['z_score'], marker='^', color='green', label='Buy Signal')
    ax2.scatter(sell_signals['time_index'], sell_signals['z_score'], marker='v', color='red', label='Sell Signal')
    ax2.scatter(exit_df['time_index'], exit_df['z_score'], marker='x', color='black', label='Exit')
    ax2.set_ylabel('Z-Score')
    ax2.set_xlabel('Time')
    ax2.set_title(f'{symbol} - Z-Score and Entry Signals')
    ax2.legend()
    ax2.grid(True)

    # Tick labels
    tick_spacing = max(1, len(df) // 10)
    tick_locs = df['time_index'][::tick_spacing]
    tick_labels = df['datetime'][::tick_spacing].dt.strftime("%m-%d %H:%M")

    ax2.set_xticks(tick_locs)
    ax2.set_xticklabels(tick_labels, rotation=45)

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