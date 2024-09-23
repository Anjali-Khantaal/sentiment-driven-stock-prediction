import pandas as pd
from config import NEWS_DATA_FILE, STOCK_DATA_FILE, MERGED_DATA_FILE

def load_data():
    # Parse dates with UTC timezone
    news_df = pd.read_csv(NEWS_DATA_FILE, parse_dates=['publishedAt'], date_parser=lambda x: pd.to_datetime(x, utc=True))
    stock_df = pd.read_csv(STOCK_DATA_FILE, parse_dates=['Datetime'], date_parser=lambda x: pd.to_datetime(x, utc=True))
    return news_df, stock_df

def integrate_data(news_df, stock_df):
    # Round news timestamps to the nearest hour
    news_df['publishedAt'] = news_df['publishedAt'].dt.floor('h')  # Updated 'H' to 'h'

    # Encode sentiments numerically
    sentiment_encoding = {'positive': 1, 'neutral': 0, 'negative': -1}
    news_df['sentiment_numeric'] = news_df['sentiment'].map(sentiment_encoding)

    # Aggregate sentiment scores by hour
    sentiment_hourly = news_df.groupby('publishedAt')['sentiment_numeric'].mean().reset_index()

    # Ensure datetime columns are sorted
    stock_df.sort_values('Datetime', inplace=True)
    sentiment_hourly.sort_values('publishedAt', inplace=True)
    
    # Debug: Check timezones
    print("news_df['publishedAt'] timezone:", news_df['publishedAt'].dt.tz)
    print("stock_df['Datetime'] timezone:", stock_df['Datetime'].dt.tz)

    # Merge with stock data using merge_asof
    merged_df = pd.merge_asof(
        stock_df,
        sentiment_hourly,
        left_on='Datetime',
        right_on='publishedAt',
        direction='backward'
    )

    # Fill missing sentiment values with 0 (neutral)
    merged_df['sentiment_numeric'].fillna(0, inplace=True)
    return merged_df

def save_data(df):
    df.to_csv(MERGED_DATA_FILE, index=False)
    print(f"Merged data saved to {MERGED_DATA_FILE}")

def main():
    news_df, stock_df = load_data()
    merged_df = integrate_data(news_df, stock_df)
    save_data(merged_df)

if __name__ == "__main__":
    main()
