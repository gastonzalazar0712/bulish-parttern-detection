# 📈 Bullish Flag Pattern Detection

This project is designed to detect **bullish flag patterns** in stock market data. Using historical stock data, the system identifies upward price movements followed by consolidation periods and breakout points. It also includes a probability calculation for the likelihood of a price rise after the breakout.

## 🛠️ Features

- Detects **bullish flag patterns** in stock prices.
- Identifies **flagpole** (upward price movement), **consolidation** (sideways or downward movement), and **breakout**.
- Uses **volume spike** confirmation during the breakout.
- Displays detected patterns in a **tabular format** and highlights breakouts on **candlestick charts**.
- Integrates with a **MySQL database** for fetching historical stock data.
- Built with **Streamlit** for an interactive web interface.

## 🚀 Installation

### Prerequisites

Make sure you have the following installed:

- Python 3.7 or higher
- MySQL database for storing historical stock data

### Install Dependencies

Clone the repository and install the required Python packages.

```bash
git clone https://github.com/your-repo/bullish-flag-pattern-detection.git
cd bullish-flag-pattern-detection
pip install -r requirements.txt
```
### Usage
```bash
streamlit run web/app.py
```
