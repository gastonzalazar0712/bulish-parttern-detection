import pandas as pd
import numpy as np
import mysql.connector
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import DB_CONFIG

def detect_all_bullish_flags(ticker):
    """
    Detects all bullish flag patterns for a given stock ticker
    and returns them in a DataFrame, including the flag's success rate.
    """
    # Connect to MySQL and fetch the stock data
    conn = mysql.connector.connect(**DB_CONFIG)
    query = f"SELECT date, close_price, volume, open_price, high_price, low_price FROM historical_data WHERE ticker='{ticker}' ORDER BY date ASC"
    df = pd.read_sql(query, conn)
    conn.close()

    # Calculate daily returns (percentage change)
    df["returns"] = df["close_price"].pct_change()

    # Manually calculate the EMA (Exponential Moving Average)
    df['ema20'] = df['close_price'].ewm(span=20, adjust=False).mean()
    df['ema50'] = df['close_price'].ewm(span=50, adjust=False).mean()

    # Calculate the Rate of Change (ROC)
    df['roc'] = df['close_price'].pct_change(periods=5)  # 5-period rate of change

    # Find bullish flag patterns
    flags = []

    for i in range(5, len(df) - 5):  # Start looking from day 5 to allow for some history
        # Flagpole: Significant upward movement (5-10% increase in 3-5 days)
        if df['close_price'][i] > df['close_price'][i - 5] * 1.05 and df['roc'][i] > 0.05:
            # Check consolidation (flag): The price should move sideways (max 10% retracement)
            flag_start = i
            flag_end = None

            # Flag detection: Prices should move within a tight range (sideways or down)
            for j in range(i + 1, len(df)):
                if df['close_price'][j] < df['close_price'][i] * 1.10 and df['close_price'][j] > df['close_price'][i] * 0.90:
                    flag_end = j
                else:
                    break

            if flag_end is not None:
                # Breakout: Price should rise above the flag resistance
                breakout_point = flag_end + 1

                # Ensure breakout_point is within bounds
                if breakout_point < len(df):
                    if df['close_price'][breakout_point] > df['close_price'][flag_end] * 1.02:
                        # Volume increase
                        if df['volume'][breakout_point] > df['volume'][breakout_point - 1] * 1.2:
                            flags.append({
                                'start_date': df['date'][flag_start],
                                'end_date': df['date'][flag_end],
                                'breakout_date': df['date'][breakout_point],
                                'flag_pole_pct': (df['close_price'][flag_end] - df['close_price'][flag_start]) / df['close_price'][flag_start],
                                'price_at_breakout': df['close_price'][breakout_point]
                            })

    # Return all the detected flags
    if len(flags) == 0:
        return pd.DataFrame()  # No flags detected
    return pd.DataFrame(flags)
