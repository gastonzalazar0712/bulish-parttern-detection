from datetime import datetime, timedelta
import mysql.connector
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import DB_CONFIG

def calculate_success_probability(ticker, flag_start, flag_end):
    """
    Calculate the probability that a bullish flag pattern will result in a price increase.
    """
    # Convert start and end dates to datetime objects for comparison
    flag_start = datetime.strptime(flag_start, '%Y-%m-%d')
    flag_end = datetime.strptime(flag_end, '%Y-%m-%d')

    # Connect to MySQL database
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Query price data after the flag pattern ends
    query = f"""
        SELECT date, close_price
        FROM historical_data
        WHERE ticker = '{ticker}' AND date BETWEEN '{flag_end}' AND '{(flag_end + timedelta(days=20)).strftime('%Y-%m-%d')}'
    """
    cursor.execute(query)
    data = cursor.fetchall()

    # Calculate the average price movement after the pattern
    price_increase = 0
    for row in data:
        date, close_price = row
        if close_price > data[0][1]:  # If the price is higher than the first date's close
            price_increase += 1

    # Calculate success probability
    total_days = len(data)
    success_probability = (price_increase / total_days) * 100 if total_days > 0 else 0

    # Close the database connection
    cursor.close()
    conn.close()

    return success_probability
