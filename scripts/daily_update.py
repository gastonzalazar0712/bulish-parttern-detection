import requests
from bs4 import BeautifulSoup
import mysql.connector
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import DB_CONFIG

# Yahoo Finance Scraper for latest data
def get_latest_price(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    try:
        price = soup.find("fin-streamer", {"data-field": "regularMarketPrice"}).text
        return float(price.replace(',', ''))
    except:
        return None

# Update DB with latest prices
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

tickers = ["AAPL", "MSFT", "SPY"]
for ticker in tickers:
    price = get_latest_price(ticker)
    print(price)
    if price:
        cursor.execute("""
            UPDATE historical_data SET close_price = %s
            WHERE ticker = %s ORDER BY date DESC LIMIT 1
        """, (price, ticker))
        conn.commit()

cursor.close()
conn.close()
