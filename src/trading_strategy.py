import pandas as pd
from config import MERGED_DATA_FILE, PORTFOLIO_DATA_FILE, INITIAL_BALANCE, TRANSACTION_COST

def load_merged_data():
    merged_df = pd.read_csv(MERGED_DATA_FILE, parse_dates=['Datetime'])
    return merged_df

def simulate_trading_strategy(merged_df):
    balance = INITIAL_BALANCE
    shares = 0
    portfolio_values = []
    total_trades = 0

    for index, row in merged_df.iterrows():
        price = row['Close']
        sentiment = row['sentiment_numeric']

        # Buy Signal
        if sentiment > 0:
            # Buy as many shares as possible
            num_shares_to_buy = int(balance // price)
            if num_shares_to_buy > 0:
                cost = num_shares_to_buy * price * (1 + TRANSACTION_COST)
                if balance >= cost:
                    shares += num_shares_to_buy
                    balance -= cost
                    total_trades += 1

        # Sell Signal
        elif sentiment < 0 and shares > 0:
            # Sell all shares
            revenue = shares * price * (1 - TRANSACTION_COST)
            balance += revenue
            shares = 0
            total_trades += 1

        # Record portfolio value
        total_value = balance + shares * price
        portfolio_values.append(total_value)

    merged_df['Portfolio Value'] = portfolio_values
    print(f"Total trades executed: {total_trades}")
    return merged_df

def save_portfolio_data(df):
    df.to_csv(PORTFOLIO_DATA_FILE, index=False)
    print(f"Portfolio data saved to {PORTFOLIO_DATA_FILE}")

def calculate_return(df):
    final_value = df['Portfolio Value'].iloc[-1]
    return_percentage = ((final_value - INITIAL_BALANCE) / INITIAL_BALANCE) * 100
    print(f"Total Return: {return_percentage:.2f}%")

def main():
    merged_df = load_merged_data()
    portfolio_df = simulate_trading_strategy(merged_df)
    save_portfolio_data(portfolio_df)
    calculate_return(portfolio_df)

if __name__ == "__main__":
    main()
