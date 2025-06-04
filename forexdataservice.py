import yfinance as yf
import requests
import pandas as pd
import requests
import time
from polygon import RESTClient

POLYGON_API_KEY = "yRQ0n7WTlfmPGzprsDfUD2vaxkXYVWZ2"
symbol = "C:GBPUSD"  # 'C:' stands for Currency
interval = "minute"
timespan = "5"
limit = 100


def fetch_forex_data(pair="GBPUSD=X", start_date="2025-04-01", interval="5m"):
    df = yf.download(pair, start=start_date, interval=interval)
    df.dropna(inplace=True)
    df.columns = df.columns.get_level_values(0)
    df.columns.name = None
    df.drop('Volume', axis=1, inplace=True)
    return df


# Fetch realtime data from PolygonIO API key = yRQ0n7WTlfmPGzprsDfUD2vaxkXYVWZ2
def fetch_realtime_forex_polygon():
    client = RESTClient(POLYGON_API_KEY)

    aggs = []
    for a in client.list_aggs(
            symbol,
            1,
            "minute",
            "2025-05-31",
            "2025-06-01",
            adjusted="true",
            sort="asc",
            limit=120,
    ):
        aggs.append(a)

    print(aggs)
    return 1


# API KEY FOR Alpha Vantage :: GRO1XE35QIUND0NW
def fetch_realtime_forex(from_symbol="EUR", to_symbol="USD", interval="1min", api_key="GRO1XE35QIUND0NW", retries=3):
    url = f"https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={from_symbol}&to_symbol={to_symbol}&interval={interval}&apikey={api_key}&outputsize=compact"

    for attempt in range(retries):
        response = requests.get(url)
        if response.status_code != 200:
            print(f"HTTP error: {response.status_code}")
            time.sleep(12)  # Wait and retry
            continue

        data = response.json()

        # API limit hit or invalid response
        if 'Note' in data or 'Error Message' in data:
            print("API limit hit or bad request. Waiting before retrying...")
            time.sleep(15)  # Wait longer before retry
            continue

        time_series = data.get(f'Time Series FX (Daily)', {})
        if not time_series:
            print("No time series data found.")
            return pd.DataFrame()

        df = pd.DataFrame.from_dict(time_series, orient='index').astype(float)
        df = df.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close'
        })
        df = df.astype(float)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()

        print(df.head())
        return df

    print("Failed to fetch data after retries.")
    return pd.DataFrame()


