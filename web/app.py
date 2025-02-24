import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import mysql.connector  # <--- Add this import
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.bullish_flag import detect_all_bullish_flags
from config import DB_CONFIG

# Page Title
st.title("📈 Stock Pattern Analysis – Bullish Flag Detector")

# Available tickers
tickers = ["SPY","AAPL", "MSFT"]

# User input: Select a stock
selected_ticker = st.selectbox("Select a Stock Ticker:", tickers)

# Detect all bullish flags for the selected ticker
st.subheader(f"📊 Bullish Flag Patterns for {selected_ticker}")
patterns = detect_all_bullish_flags(selected_ticker)

if patterns.empty:
    st.write("❌ No Bullish Flag patterns detected.")
else:
    st.write(f"✅ {len(patterns)} occurrences found.")
    st.dataframe(patterns)  # Show a table of all detected bullish flags

    # Plot the last detection (optional)
    last_detection = patterns.iloc[-1]
    # Plot the price data and highlight the detected bullish flag
    conn = mysql.connector.connect(**DB_CONFIG)
    query = f"SELECT date, close_price FROM historical_data WHERE ticker='{selected_ticker}' ORDER BY date ASC"
    df = pd.read_sql(query, conn)
    conn.close()

    fig = go.Figure(data=[go.Candlestick(
        x=df['date'],
        open=df['close_price'],  # You should use open, high, low, close here
        high=df['close_price'],
        low=df['close_price'],
        close=df['close_price']
    )])

    # Add the breakout point to the graph
    fig.add_trace(go.Scatter(x=[last_detection['breakout_date']], y=[last_detection['price_at_breakout']], mode='markers', marker=dict(color='red', size=12)))
    st.plotly_chart(fig)
