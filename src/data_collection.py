import os
import requests
import pandas as pd
from datetime import datetime
from config import API_KEY, COMPANY_NAME, FROM_DATE, TO_DATE, NEWS_DATA_FILE, STOCK_TICKER, STOCK_DATA_FILE

def fetch_news_data():
    url = (
        'https://newsapi.org/v2/everything?'
        f'q={COMPANY_NAME}&from={FROM_DATE}&to={TO_DATE}&sortBy=popularity&'
        f'apiKey={API_KEY}'
    )

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        if not articles:
            print("No articles found for the given parameters.")
            return None
        else:
            news_df = pd.DataFrame(articles)
            news_df = news_df[['publishedAt', 'title']]
            # Parse 'publishedAt' with UTC timezone
            news_df['publishedAt'] = pd.to_datetime(news_df['publishedAt'], utc=True)
            return news_df
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def fetch_stock_data():
    import yfinance as yf

    stock_data = yf.download(
        STOCK_TICKER,
        start=FROM_DATE,
        end=TO_DATE,
        interval='1h',
        progress=False
    )
    stock_data.reset_index(inplace=True)
    stock_data.dropna(inplace=True)
    # Ensure 'Datetime' is timezone-aware and set to UTC
    stock_data['Datetime'] = pd.to_datetime(stock_data['Datetime'], utc=True)
    return stock_data

def save_data(df, file_path):
    df.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

def main():
    # Ensure data directory exists
    os.makedirs(os.path.dirname(NEWS_DATA_FILE), exist_ok=True)

    # Fetch and save news data
    news_df = fetch_news_data()
    if news_df is not None:
        save_data(news_df, NEWS_DATA_FILE)

    # Fetch and save stock data
    stock_df = fetch_stock_data()
    if not stock_df.empty:
        save_data(stock_df, STOCK_DATA_FILE)
    else:
        print("No stock data fetched.")

if __name__ == "__main__":
    main()
