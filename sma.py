import sqlite3
import pandas as pd
import numpy as np
import datetime
from kiteconnect import KiteConnect
import time
import matplotlib.pyplot as plt

API_KEY = "8kb1ag60chrc88ol"
API_SECRET = "26y0pw6mdwkurjn6e2z01hqtxti942zj"
ACCESS_TOKEN = "nO2f4HtuMdgVz5lmORK3kVJbQ20ShpQO"
DB_PATH = "intraday_stock_data.db"

# Intraday Config
SMA_SHORT = 10
SMA_LONG = 30
INTERVAL = "5minute"
DATE_RANGE_DAYS = 5

# Stock universe
STOCK_LIST = ["RELIANCE", "VOLTAS", "TATVA"]
EXCHANGE = "NSE"

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock_data (
            symbol TEXT,
            datetime TEXT,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            sma_short REAL,
            sma_long REAL,
            signal TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_token(symbol):
    instruments = kite.instruments(EXCHANGE)
    for i in instruments:
        if i['tradingsymbol'] == symbol:
            return i['instrument_token']
    raise Exception(f"Instrument token not found for {symbol}")

def fetch_intraday_data(symbol):
    token = get_token(symbol)
    to_date = datetime.datetime.now()
    from_date = to_date - datetime.timedelta(days=DATE_RANGE_DAYS)
    
    data = kite.historical_data(token, from_date, to_date, INTERVAL)
    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['date'])
    df.drop(columns=['date'], inplace=True)
    return df

def process_and_store(symbol, df):
    df['sma_short'] = df['close'].rolling(SMA_SHORT).mean()
    df['sma_long'] = df['close'].rolling(SMA_LONG).mean()
    df['signal'] = np.where(df['sma_short'] > df['sma_long'], 'BUY', 'SELL')
    df['symbol'] = symbol
    df = df[['symbol', 'datetime', 'open', 'high', 'low', 'close', 'volume', 'sma_short', 'sma_long', 'signal']]

    conn = sqlite3.connect(DB_PATH)
    df.to_sql('stock_data', conn, if_exists='append', index=False)
    conn.close()
    print(f"Saved {symbol} data to DB.")

def run_backtest(symbol):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(f"SELECT * FROM stock_data WHERE symbol = '{symbol}'", conn, parse_dates=['datetime'])
    conn.close()

    df = df.dropna()
    df['position'] = df['signal'].shift()
    df['returns'] = df['close'].pct_change()
    df['strategy_returns'] = df['returns'] * np.where(df['position'] == 'BUY', 1, 0)
    df['cumulative_market_returns'] = (1 + df['returns']).cumprod()
    df['cumulative_strategy_returns'] = (1 + df['strategy_returns']).cumprod()

    print(f"\n[{symbol}]")
    print("Final Strategy Return:", round(df['cumulative_strategy_returns'].iloc[-1], 4))
    print("Final Market Return:", round(df['cumulative_market_returns'].iloc[-1], 4))

    plt.figure(figsize=(10, 4))
    plt.plot(df['datetime'], df['cumulative_market_returns'], label="Market")
    plt.plot(df['datetime'], df['cumulative_strategy_returns'], label="Strategy")
    plt.title(f"{symbol} - Intraday SMA Backtest")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Returns")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    init_db()
    for symbol in STOCK_LIST:
        try:
            print(f"\nFetching data for {symbol}...")
            df = fetch_intraday_data(symbol)
            process_and_store(symbol, df)
            run_backtest(symbol)
            time.sleep(2)  # Respect API rate limits
        except Exception as e:
            print(f"Error with {symbol}: {str(e)}")
