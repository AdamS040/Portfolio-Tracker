# src/data_fetcher.py
from typing import List, Optional

import pandas as pd
import yfinance as yf


def fetch_price_history(
    tickers: List[str],
    start: str,
    end: Optional[str] = None,
) -> pd.DataFrame:
    """
    Returns a DataFrame of adjusted close prices for tickers between start and end.
    Ensures a 2D DataFrame even for a single ticker.

    Columns: one per ticker
    Index: DatetimeIndex
    """
    data = yf.download(
        tickers,
        start=start,
        end=end,
        progress=False,
        auto_adjust=False,
        group_by="column",
        threads=True,
    )

    # yfinance returns different shapes depending on number of tickers
    adj = data["Adj Close"]
    if isinstance(adj, pd.Series):
        # Single ticker -> make into DataFrame with column name as ticker
        adj = adj.to_frame(name=tickers[0])

    # Ensure columns are exactly the tickers order where possible
    # (some tickers may be missing if invalid)
    present = [c for c in tickers if c in adj.columns]
    adj = adj[present]

    adj = adj.sort_index()
    return adj
