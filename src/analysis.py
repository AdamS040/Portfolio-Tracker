# src/analysis.py

from src.data_fetcher import fetch_price_history, fetch_benchmark
from src.portfolio import compute_positions
from src.metrics import sharpe_ratio, max_drawdown, alpha_beta

def analyze_portfolio(pf, rf, bench, start_date='2023-01-01', end_date='2025-06-25'):
    """
    Perform portfolio analysis:
    - Fetch prices
    - Compute returns
    - Calculate Sharpe Ratio, Max Drawdown, Alpha & Beta
    - Prepare cumulative returns for plotting

    Args:
        pf (pd.DataFrame): Portfolio dataframe with 'ticker' and 'weight' columns
        rf (float): Risk-free rate (annualized decimal, e.g. 0.01 for 1%)
        bench (str): Benchmark ticker symbol (e.g. 'SPY')
        start_date (str): Price data start date
        end_date (str): Price data end date

    Returns:
        tuple: (sharpe_ratio, max_drawdown, alpha_beta_dict, cum_port, cum_bench, port_returns)
    """
    tickers = pf['ticker'].tolist() + [bench]

    # Fetch historical price data for all tickers
    prices = fetch_price_history(tickers, start=start_date, end=end_date)

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
