import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from config import PORTFOLIO_DATA_FILE

def load_portfolio_data():
    df = pd.read_csv(PORTFOLIO_DATA_FILE, parse_dates=['Datetime'])
    return df

def plot_sentiment_distribution(df):
    plt.figure(figsize=(8, 6))
    sns.countplot(x='sentiment_numeric', data=df)
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.xticks(ticks=[0, 1, 2], labels=['Negative', 'Neutral', 'Positive'])
    plt.tight_layout()
    plt.savefig('../figures/sentiment_distribution.png')
    plt.close()
    print("Sentiment distribution plot saved.")

def plot_stock_price(df):
    plt.figure(figsize=(14, 7))
    sns.lineplot(x='Datetime', y='Close', data=df)
    plt.title('Stock Price Over Time')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.tight_layout()
    plt.savefig('../figures/stock_price.png')
    plt.close()
    print("Stock price plot saved.")

def plot_portfolio_value(df):
    plt.figure(figsize=(14, 7))
    sns.lineplot(x='Datetime', y='Portfolio Value', data=df)
    plt.title('Portfolio Value Over Time')
    plt.xlabel('Date')
    plt.ylabel('Value ($)')
    plt.tight_layout()
    plt.savefig('../figures/portfolio_value.png')
    plt.close()
    print("Portfolio value plot saved.")

def main():
    df = load_portfolio_data()
    plot_sentiment_distribution(df)
    plot_stock_price(df)
    plot_portfolio_value(df)

if __name__ == "__main__":
    main()
