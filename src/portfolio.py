import pandas as pd
from typing import Dict

def load_portfolio(path: str) -> pd.DataFrame:
    """
    Expects CSV with columns: ticker, weight (or shares), type [real|mock].
    """
    df = pd.read_csv(path)
    # Validate columns...
    return df

def compute_positions(
    prices: pd.DataFrame,
    portfolio: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate daily portfolio value based on weights or shares.
    """
    if 'weight' in portfolio:
        weights = portfolio.set_index('ticker')['weight']
        prices_filled = prices.ffill()
        returns = prices_filled.pct_change().dropna()
        port_returns = (returns * weights).sum(axis=1)
        return port_returns

