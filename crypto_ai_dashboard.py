# crypto_ai_dashboard.py

import streamlit as st
from crypto_ai_core import fetch_ohlcv, add_technical_indicators, basic_moving_average_strategy
import matplotlib.pyplot as plt

st.title("📈 Crypto AI Dashboard")
symbol = st.text_input("Enter Symbol", value="BTC/USD")

def color_signal(val):
    color = 'green' if val == 'BUY' else 'red' if val == 'SELL' else 'gray'
    return f'color: {color}'

if st.button("Run Analysis"):
    df = fetch_ohlcv(symbol)
    if not df.empty:
        df = add_technical_indicators(df)
        df = basic_moving_average_strategy(df)
        st.dataframe(df.tail().style.applymap(color_signal, subset=['action']))

        fig, ax = plt.subplots(figsize=(10,5))
        ax.plot(df['timestamp'], df['close'], label='Close', color='blue')
        ax.plot(df['timestamp'], df['SMA20'], label='SMA20', color='orange')
        ax.plot(df['timestamp'], df['SMA50'], label='SMA50', color='magenta')

        for i in range(1, len(df)):
            if df['action'].iloc[i] == 'BUY':
                ax.annotate('BUY', (i, df['close'].iloc[i]), color='green', fontsize=8, rotation=90)
            elif df['action'].iloc[i] == 'SELL':
                ax.annotate('SELL', (i, df['close'].iloc[i]), color='red', fontsize=8, rotation=90)

        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("No data available!")