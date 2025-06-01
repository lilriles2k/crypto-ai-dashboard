# crypto_ai_dashboard.py

import streamlit as st
from crypto_ai_core import fetch_ohlcv, add_technical_indicators, basic_moving_average_strategy
import matplotlib.pyplot as plt

st.title("📈 Crypto AI Dashboard")
symbol = st.text_input("Enter Symbol", value="BTC/USD")

if st.button("Run Analysis"):
    df = fetch_ohlcv(symbol)
    if not df.empty:
        df = add_technical_indicators(df)
        df = basic_moving_average_strategy(df)
        st.write(df.tail())

        fig, ax = plt.subplots()
        ax.plot(df['timestamp'], df['close'], label='Close')
        ax.plot(df['timestamp'], df['SMA20'], label='SMA20')
        ax.plot(df['timestamp'], df['SMA50'], label='SMA50')

        for i in range(1, len(df)):
            if df['action'].iloc[i] == 'BUY':
                ax.annotate('BUY', (df['timestamp'].iloc[i], df['close'].iloc[i]), color='green', fontsize=8, rotation=90)
            elif df['action'].iloc[i] == 'SELL':
                ax.annotate('SELL', (df['timestamp'].iloc[i], df['close'].iloc[i]), color='red', fontsize=8, rotation=90)

        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("No data available!")