import yfinance as yf
import mysql.connector
import pandas as pd

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config import DB_CONFIG


# Connect to MySQL
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Function to insert stock ticker into stocks table
def insert_stock_ticker(ticker):
    stock = yf.Ticker(ticker)
    company_name = stock.info.get("longName", "Unknown")
    sector = stock.info.get("sector", "Unknown")

    cursor.execute("""
        INSERT INTO stocks (ticker, company_name, sector)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE company_name=%s, sector=%s
    """, (ticker, company_name, sector, company_name, sector))
    conn.commit()

# Function to insert historical stock data
def insert_stock_data(ticker):
    # Ensure ticker exists in stocks table
    insert_stock_ticker(ticker)
    
    stock = yf.Ticker(ticker)
    df = stock.history(period="3d")  
    
    
    df.reset_index(inplace=True)
    for _, row in df.iterrows():
        print(1)
        cursor.execute("""
            INSERT INTO historical_data (ticker, date, open_price, high_price, low_price, close_price, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE close_price=%s, volume=%s
        """, (ticker, row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], row['Close'], row['Volume']))
    
    conn.commit()

# Load data for multiple tickers
tickers = ["AAPL", "MSFT", "SPY"]  # Add more tickers if needed
for ticker in tickers:
    insert_stock_data(ticker)

cursor.close()
conn.close()
