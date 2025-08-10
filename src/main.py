import argparse
import yaml
import os
import sys
import pandas as pd

from data_fetcher import fetch_price_history, fetch_benchmark
from portfolio import load_portfolio, compute_positions
from metrics import sharpe_ratio, max_drawdown, alpha_beta
from visualization import plot_cumulative_returns, plot_drawdown, plot_rolling_volatility


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--portfolio', required=True, help='Path to portfolio CSV')
    args = parser.parse_args()

    # ===== CONFIG FILE CHECK =====
    config_path = 'config/config.yaml'
    if not os.path.exists(config_path):
        sys.exit(f"❌ ERROR: Config file not found at '{config_path}'. Please create it before running.")

    try:
        with open(config_path, 'r') as f:
            cfg = yaml.safe_load(f)
    except yaml.YAMLError as e:
        sys.exit(f"❌ ERROR: Failed to parse YAML config: {e}")

    if not isinstance(cfg, dict) or 'risk_free_rate' not in cfg or 'benchmark' not in cfg:
        sys.exit("❌ ERROR: Config file must contain 'risk_free_rate' and 'benchmark'.")

    rf = cfg['risk_free_rate']
    bench = cfg['benchmark']

    # ===== PORTFOLIO CSV CHECK =====
    if not os.path.exists(args.portfolio):
        sys.exit(f"❌ ERROR: Portfolio CSV file not found at '{args.portfolio}'.")

    try:
        pf = load_portfolio(args.portfolio)
    except Exception as e:
        sys.exit(f"❌ ERROR: Failed to load portfolio CSV: {e}")

    if 'ticker' not in pf.columns:
        sys.exit("❌ ERROR: Portfolio CSV must contain a 'ticker' column.")

    # ===== DATA FETCHING =====
    tickers = pf['ticker'].tolist() + [bench]
    prices = fetch_price_history(tickers, start='2023-01-01', end='2025-06-25')

    port_returns = compute_positions(prices.drop(columns=[bench]), pf)
    bench_returns = fetch_benchmark(bench, '2023-01-01', '2025-06-25').pct_change().dropna()

    # ===== METRICS =====
    sr = sharpe_ratio(port_returns, rf)
    mdd = max_drawdown(port_returns)
    ab = alpha_beta(port_returns, bench_returns)

    print(f"Sharpe Ratio: {sr:.2f}")
    print(f"Max Drawdown: {mdd:.2%}")
    print(f"Alpha: {ab['alpha']:.2%}, Beta: {ab['beta']:.2f}")

    # ===== VISUALIZATION =====
    cum_port = (1 + port_returns).cumprod()
    cum_bench = (1 + bench_returns).cumprod()

    plot_cumulative_returns(cum_port, cum_bench)
    plot_drawdown(cum_port)
    plot_rolling_volatility(port_returns)


if __name__ == '__main__':
    main()
