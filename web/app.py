import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.bullish_flag import detect_most_recent_bullish_flag
from models.pattern_probability import calculate_success_probability
import mysql.connector
from config import DB_CONFIG

# Page Title
st.title("📈 Stock Pattern Analysis – Most Recent Bullish Flag Detector")

# Available tickers
tickers = ["AAPL", "MSFT", "SPY"]

# User input: Select a stock
selected_ticker = st.selectbox("Select a Stock Ticker:", tickers)

# Connect to MySQL to fetch historical data
def fetch_stock_data(ticker):
    conn = mysql.connector.connect(**DB_CONFIG)
    query = f"SELECT date, open_price, high_price, low_price, close_price FROM historical_data WHERE ticker='{ticker}' ORDER BY date ASC"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fetch data and detect bullish flag
df = fetch_stock_data(selected_ticker)
latest_pattern = detect_most_recent_bullish_flag(selected_ticker)

# Detect Most Recent Bullish Flag
st.subheader(f"📊 Most Recent Bullish Flag for {selected_ticker}")

if latest_pattern is None:
    st.write("❌ No Bullish Flag detected recently.")
else:
    st.write(f"✅ Bullish Flag detected on **{latest_pattern['date']}**")
    st.write(f"📊 Closing Price: **${latest_pattern['close_price']:.2f}**")

    # Plot stock price data with Plotly
    fig = go.Figure()

    # Add candlestick chart
    fig.add_trace(go.Candlestick(
        x=df["date"],
        open=df["open_price"],
        high=df["high_price"],
        low=df["low_price"],
        close=df["close_price"],
        name="Stock Price"
    ))

    # Highlight the bullish flag pattern
    fig.add_trace(go.Scatter(
        x=[latest_pattern["date"]],
        y=[latest_pattern["close_price"]],
        mode="markers",
        marker=dict(color="red", size=10),
        name="Bullish Flag"
    ))

    fig.update_layout(
        title=f"{selected_ticker} Stock Price with Most Recent Bullish Flag",
        xaxis_title="Date",
        yaxis_title="Stock Price (USD)",
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig)

# Calculate Probability of Success
st.subheader(f"📈 Probability of Bullish Flag Leading to Price Increase")
probability = calculate_success_probability(selected_ticker)

if probability == 0:
    st.write("⚠️ Not enough data to determine probability.")
else:
    st.write(f"📊 **{selected_ticker} - Probability of Success: {probability:.2%}**")

# Notes
st.info("🔍 The analysis is based on historical stock data and may not guarantee future price movements.")
