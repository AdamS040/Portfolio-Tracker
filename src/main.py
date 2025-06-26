import argparse
import yaml
from data_fetcher import fetch_price_history, fetch_benchmark
from portfolio import load_portfolio, compute_positions
from metrics import sharpe_ratio, max_drawdown, alpha_beta
from visualization import plot_cumulative_returns

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--portfolio', required=True, help='path to portfolio CSV')
    args = parser.parse_args()

    # Load config
    cfg = yaml.safe_load(open('config/config.yaml'))
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
