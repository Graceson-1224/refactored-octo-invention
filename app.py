import streamlit as st
import pandas as pd
import requests
import plotly.graph_objs as go
from datetime import datetime, timedelta

# --- SETTINGS ---
st.set_page_config(layout="wide")
API_KEY = "demo"  # Replace with your own from https://www.alphavantage.co
BASE_URL = "https://www.alphavantage.co/query"

# --- FUNCTION TO GET STOCK DATA ---
@st.cache_data(ttl=300)
def get_stock_data(symbol):
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if "Time Series (5min)" not in data:
        return None

    df = pd.DataFrame.from_dict(data["Time Series (5min)"], orient="index", dtype=float)
    df.columns = ["Open", "High", "Low", "Close", "Volume"]
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    return df

# --- DASHBOARD UI ---
st.title("📈 Real-Time Stock Market Dashboard")

stock = st.text_input("Enter Stock Symbol (e.g. AAPL, MSFT, TSLA)", "AAPL")

df = get_stock_data(stock)

if df is not None:
    st.subheader(f"Latest Stock Data for {stock.upper()}")
    st.write(df.tail())

    # Plot Closing Price
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Close"))
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"].rolling(5).mean(), mode="lines", name="MA 5"))
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"].rolling(10).mean(), mode="lines", name="MA 10"))

    fig.update_layout(title="Stock Price Over Time", xaxis_title="Time", yaxis_title="Price ($)", height=500)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("Error fetching stock data. Try a valid stock symbol.")

