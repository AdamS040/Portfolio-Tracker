# src/analysis.py
from typing import Tuple, Dict

import pandas as pd

from src.data_fetcher import fetch_price_history
from src.portfolio import compute_positions
from src.metrics import sharpe_ratio, max_drawdown, alpha_beta


def analyze_portfolio(
    pf: pd.DataFrame,
    risk_free_rate: float,
    benchmark: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> Tuple[float, float, Dict[str, float], pd.Series, pd.Series, pd.Series]:
    """
    End-to-end portfolio analysis. Downloads prices once (portfolio + benchmark),
    computes returns, then metrics and cumulative series.

    Returns:
        sr (float): Sharpe ratio
        mdd (float): Max drawdown (negative number)
        ab (dict): {'alpha': float, 'beta': float}
        cum_port (pd.Series): Portfolio cumulative returns
        cum_bench (pd.Series): Benchmark cumulative returns
        port_returns (pd.Series): Daily portfolio returns
    """
    if start_date is None:
        start_date = "2023-01-01"

    tickers = pf["ticker"].tolist()
    all_tickers = list(dict.fromkeys(tickers + [benchmark]))  # preserve order, unique

    prices = fetch_price_history(all_tickers, start=start_date, end=end_date)

    # Split portfolio vs. benchmark
    bench_prices = prices[benchmark]
    pf_prices = prices.drop(columns=[benchmark], errors="ignore")

    # Portfolio daily returns from component prices & weights
    port_returns = compute_positions(pf_prices, pf)

    # Benchmark daily returns
    bench_returns = bench_prices.pct_change().dropna()

    # Metrics
    sr = sharpe_ratio(port_returns, risk_free_rate)
    mdd = max_drawdown(port_returns)
    ab = alpha_beta(port_returns, bench_returns, risk_free_rate=risk_free_rate)

    # Cumulative for plotting
    cum_port = (1 + port_returns).cumprod()
    cum_bench = (1 + bench_returns).cumprod()

    return sr, mdd, ab, cum_port, cum_bench, port_returns
