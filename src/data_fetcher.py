```python
import yfinance as yf
import pandas as pd
from typing import List, Tuple

def fetch_price_history(
    tickers: List[str],
    start: str,
    end: str
) -> pd.DataFrame:
    """
    Returns adjusted close prices for tickers between start and end.
    """
    data = yf.download(tickers, start=start, end=end, progress=False)
    return data['Adj Close']

def fetch_benchmark(
    benchmark_ticker: str,
    start: str,
    end: str
) -> pd.Series:
    """Fetches benchmark adjusted close price series."""
    return fetch_price_history([benchmark_ticker], start, end).squeeze()
