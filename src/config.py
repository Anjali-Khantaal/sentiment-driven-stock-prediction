import os
from datetime import datetime, timedelta

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# API Key
API_KEY = os.getenv('NEWSAPI_KEY')

# Company and Stock Ticker
COMPANY_NAME = 'Apple Inc'
STOCK_TICKER = 'AAPL'

# Date Range for Data Collection
TODAY = datetime.today()
FROM_DATE = (TODAY - timedelta(days=7)).strftime('%Y-%m-%d')
TO_DATE = TODAY.strftime('%Y-%m-%d')

# Data Directories
DATA_DIR = '../data/'
NEWS_DATA_FILE = os.path.join(DATA_DIR, 'news_data.csv')
STOCK_DATA_FILE = os.path.join(DATA_DIR, 'stock_data.csv')
MERGED_DATA_FILE = os.path.join(DATA_DIR, 'merged_data.csv')
PORTFOLIO_DATA_FILE = os.path.join(DATA_DIR, 'portfolio_data.csv')

# Model Parameters
MAX_SEQ_LENGTH = 64

# Trading Strategy Parameters
INITIAL_BALANCE = 10000  # Starting with $10,000
TRANSACTION_COST = 0.001  # 0.1% per trade
