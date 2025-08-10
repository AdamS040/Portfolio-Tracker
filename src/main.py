import argparse
import yaml
from data_fetcher import fetch_price_history, fetch_benchmark
from portfolio import load_portfolio, compute_positions
from metrics import sharpe_ratio, max_drawdown, alpha_beta
from visualization import plot_cumulative_returns
import os
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--portfolio', required=True, help='path to portfolio CSV')
    args = parser.parse_args()

    # Load config
config_path = 'config/config.yaml'
if not os.path.exists(config_path):
    sys.exit(f"❌ ERROR: Config file not found at '{config_path}'. Please create it before running.")
try:
    with open(config_path, 'r') as f:
        cfg = yaml.safe_load(f)
except yaml.YAMLError as e:
    sys.exit(f"❌ ERROR: Failed to parse YAML config: {e}")

if 'risk_free_rate' not in cfg or 'benchmark' not in cfg:
    sys.exit("❌ ERROR: Config file must contain 'risk_free_rate' and 'benchmark'.")

    rf = cfg['risk_free_rate']
    bench = cfg['benchmark']

    # 1. Load portfolio
    pf = load_portfolio(args.portfolio)

    # 2. Fetch data
    tickers = pf['ticker'].tolist() + [bench]
    prices = fetch_price_history(tickers, start='2023-01-01', end='2025-06-25')

    # 3. Compute returns
    port_returns = compute_positions(prices.drop(columns=[bench]), pf)
    bench_returns = fetch_benchmark(bench, '2023-01-01', '2025-06-25').pct_change().dropna()

    # 4. Metrics
    sr = sharpe_ratio(port_returns, rf)
    mdd = max_drawdown(port_returns)
    ab = alpha_beta(port_returns, bench_returns)

    print(f"Sharpe Ratio: {sr:.2f}")
    print(f"Max Drawdown: {mdd:.2%}")
    print(f"Alpha: {ab['alpha']:.2%}, Beta: {ab['beta']:.2f}")

    # 5. Visualization
    plot_cumulative_returns((1+port_returns).cumprod(),
                            (1+bench_returns).cumprod())

if __name__ == '__main__':
    main()

