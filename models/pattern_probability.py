import pandas as pd
import numpy as np
import mysql.connector
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import DB_CONFIG

def calculate_success_probability(ticker):
    conn = mysql.connector.connect(**DB_CONFIG)
    query = f"SELECT date, close_price FROM historical_data WHERE ticker='{ticker}' ORDER BY date ASC"
    df = pd.read_sql(query, conn)
    conn.close()

    df["returns"] = df["close_price"].pct_change()
    df["flag"] = np.where((df["returns"].rolling(5).mean() > 0.02) & (df["returns"].rolling(5).std() < 0.015), 1, 0)

    success = 0
    total = 0

    for i in range(len(df) - 10):
        if df["flag"].iloc[i] == 1:
            total += 1
            if df["close_price"].iloc[i+5] > df["close_price"].iloc[i]:  # Check price 5 days after pattern
                success += 1

    probability = success / total if total > 0 else 0
    return probability

tickers = ["AAPL", "MSFT", "SPY"]
for ticker in tickers:
    prob = calculate_success_probability(ticker)
    print(f"Probability of Bullish Flag Success for {ticker}: {prob:.2%}")
