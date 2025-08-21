# src/portfolio.py
import pandas as pd


def load_portfolio(path: str) -> pd.DataFrame:
    """
    Load a CSV containing columns: ticker, weight
    """
    df = pd.read_csv(path)
    return df


def compute_positions(
    prices: pd.DataFrame,
    portfolio: pd.DataFrame,
) -> pd.Series:
    """
    Compute daily portfolio returns using weights.

    Args:
        prices: DataFrame of asset prices (columns=tickers)
        portfolio: DataFrame with columns ['ticker', 'weight']

    Returns:
        pd.Series of daily portfolio returns.
    """
    if not {"ticker", "weight"}.issubset(portfolio.columns):
        raise ValueError("Portfolio must contain 'ticker' and 'weight' columns.")

    # Keep only tickers that appear in the price matrix
    weights = (
        portfolio.set_index("ticker")["weight"]
        .loc[portfolio["ticker"].unique()]
        .dropna()
    )

    weights = weights[weights.index.isin(prices.columns)]

    if weights.empty:
        raise ValueError("None of the portfolio tickers are present in price data.")

    prices_filled = prices[weights.index].ffill()
    returns = prices_filled.pct_change().dropna()

    # Normalize weights to sum to 1 (defensive if CSV doesn't)
    if not (abs(weights.sum() - 1.0) < 1e-8):
        weights = weights / weights.sum()

    port_returns = (returns * weights).sum(axis=1)
    return port_returns
