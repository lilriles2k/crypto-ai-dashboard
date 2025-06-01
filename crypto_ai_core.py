# crypto_ai_core.py

import ccxt
import pandas as pd
import numpy as np
from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

exchange = ccxt.binanceus({'enableRateLimit': True})

def fetch_ohlcv(symbol="BTC/USD", timeframe="1m", limit=100):
    try:
        data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True).dt.strftime('%Y-%m-%d %H:%M:%S')
        df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
        return df
    except Exception as e:
        print(f"Error fetching OHLCV data: {e}")
        return pd.DataFrame()

def add_technical_indicators(df):
    df = df.copy()
    df['rsi'] = RSIIndicator(close=df['close']).rsi()
    macd = MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    bb = BollingerBands(close=df['close'])
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    return df

def basic_moving_average_strategy(df):
    if df.empty or len(df) < 50:
        print("Insufficient data for strategy.")
        return pd.DataFrame()

    df = df.copy()
    df['SMA20'] = df['close'].rolling(window=20).mean()
    df['SMA50'] = df['close'].rolling(window=50).mean()
    df['signal'] = np.where(df['SMA20'] > df['SMA50'], 'BUY', 'SELL')
    df['action'] = df['signal'].shift(1).fillna("HOLD")
    return df[['timestamp', 'close', 'SMA20', 'SMA50', 'signal', 'action', 'rsi', 'macd', 'macd_signal', 'bb_upper', 'bb_lower']]

if __name__ == "__main__":
    symbol = "BTC/USD"
    print(f"Fetching data for {symbol}...")
    df = fetch_ohlcv(symbol)
    if not df.empty:
        df = add_technical_indicators(df)
        df_signals = basic_moving_average_strategy(df)
        print(df_signals.tail())
    else:
        print("No data available to generate signals.")