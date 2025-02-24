import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import DB_CONFIG

def detect_most_recent_bullish_flag(ticker):
    """
    Detects the most recent bullish flag pattern in the historical stock data for a given ticker.
    Returns the latest occurrence if found, otherwise returns None.
    """
    # Use SQLAlchemy for MySQL connection
    engine = create_engine(f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}")
    query = f"SELECT date, open_price, high_price, low_price, close_price FROM historical_data WHERE ticker='{ticker}' ORDER BY date ASC"
    df = pd.read_sql(query, engine)

    # Ensure we have enough data
    if df.shape[0] < 50:
        return None

    # Calculate key technical indicators
    df["ema_20"] = df["close_price"].ewm(span=20, adjust=False).mean()  # Short-term trend
    df["ema_50"] = df["close_price"].ewm(span=50, adjust=False).mean()  # Long-term trend
    df["returns"] = df["close_price"].pct_change()  # Daily return %

    # Identify flagpole: Look for a sharp price increase (>5% in 5 days)
    df["flagpole"] = (df["returns"].rolling(5).sum() > 0.05).astype(bool)

    # Identify consolidation (flag): The price should stay in a descending channel
    df["consolidation"] = ((df["high_price"].rolling(3).max() - df["low_price"].rolling(3).min()) / df["low_price"].rolling(3).min() < 0.03).astype(bool)

    # Identify breakout: Price moves above recent resistance
    df["breakout"] = ((df["close_price"] > df["ema_20"]) & (df["close_price"] > df["ema_50"])).astype(bool)

    # Find bullish flags (flagpole + consolidation + breakout)
    df["bullish_flag"] = df["flagpole"].shift(3).fillna(False).astype(bool) & df["consolidation"] & df["breakout"]

    bullish_flags = df[df["bullish_flag"] == True]

    if not bullish_flags.empty:
        most_recent_flag = bullish_flags.iloc[-1]  # Get the most recent occurrence
        return most_recent_flag
    else:
        return None
