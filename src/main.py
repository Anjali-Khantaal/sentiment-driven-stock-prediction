from data_collection import main as collect_data
from sentiment_analysis import main as analyze_sentiment
from data_integration import main as integrate_data
from trading_strategy import main as simulate_strategy
from visualization import main as generate_visualizations

def main():
    print("Starting data collection...")
    collect_data()

    print("\nStarting sentiment analysis...")
    analyze_sentiment()

    print("\nIntegrating data...")
    integrate_data()

    print("\nSimulating trading strategy...")
    simulate_strategy()

    print("\nGenerating visualizations...")
    generate_visualizations()

    print("\nAll steps completed successfully.")

if __name__ == "__main__":
    main()
