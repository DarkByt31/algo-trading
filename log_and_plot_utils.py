import matplotlib.pyplot as plt
import pandas as pd

def print_trade_log(symbol, trades, capital, initial_capital):
    print(f"\n[{symbol}]")
    print(f"Net Capital After Backtest: ₹{round(capital, 2)}")
    print(f"Net Profit: ₹{round(capital - initial_capital, 2)}")
    print(f"\nExecuted Trades: {len(trades)}")
    for t in trades:
        print(f"{t['time']} - {t['type']} - Qty: {t['qty']} @ ₹{t['price']} | Capital: ₹{round(t['capital'], 2)}")

def plot_mean_reversion_signals(symbol, df, trades, Z_ENTRY):
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

def plot_weekly_gains(trades, initial_capital):
    # Create DataFrame from trades
    trade_df = pd.DataFrame(trades)
    if trade_df.empty:
        print("No trades to plot weekly gains/losses.")
        return
    # Remove timezone info to avoid warning
    trade_df['week'] = pd.to_datetime(trade_df['time']).dt.tz_localize(None).dt.to_period('W').apply(lambda r: r.start_time)
    # Only consider EXIT trades for realized P&L
    exit_trades = trade_df[trade_df['type'] == 'EXIT']
    if exit_trades.empty:
        print("No EXIT trades to plot weekly gains/losses.")
        return
    # Calculate weekly capital change
    weekly_capital = exit_trades.groupby('week')['capital'].last().sort_index()
    weekly_capital = weekly_capital.reindex(pd.date_range(weekly_capital.index.min(), weekly_capital.index.max(), freq='W-MON'), method='ffill')
    weekly_capital = weekly_capital.fillna(method='ffill')
    weekly_gains = weekly_capital.diff().fillna(weekly_capital.iloc[0] - initial_capital)
    plt.figure(figsize=(10, 4))
    weekly_gains.plot(kind='bar', color=['green' if x >= 0 else 'red' for x in weekly_gains])
    plt.title('Weekly Gains/Losses')
    plt.ylabel('Net Gain/Loss (₹)')
    plt.xlabel('Week')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
