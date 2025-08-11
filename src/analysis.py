# src/analysis.py

from src.data_fetcher import fetch_price_history, fetch_benchmark
from src.portfolio import compute_positions
from src.metrics import sharpe_ratio, max_drawdown, alpha_beta

def analyze_portfolio(pf, rf, bench, start_date=None, end_date=None):
    # Use start_date and end_date to fetch price data within that range
    # Default to some sensible range if None

    # For example, pass start and end dates into data fetchers here:
    tickers = pf['ticker'].tolist() + [bench]
    prices = fetch_price_history(tickers, start=start_date or '2023-01-01', end=end_date or '2025-06-25')

    # Compute portfolio daily returns from prices and weights
    port_returns = compute_positions(prices.drop(columns=[bench]), pf)

    # Get benchmark daily returns
    bench_prices = fetch_benchmark(bench, start=start_date, end=end_date)
    bench_returns = bench_prices.pct_change().dropna()

    # Calculate performance metrics
    sr = sharpe_ratio(port_returns, rf)
    mdd = max_drawdown(port_returns)
    ab = alpha_beta(port_returns, bench_returns)

    # Calculate cumulative returns for plotting
    cum_port = (1 + port_returns).cumprod()
    cum_bench = (1 + bench_returns).cumprod()

    return sr, mdd, ab, cum_port, cum_bench, port_returns
