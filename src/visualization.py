import matplotlib.pyplot as plt
import pandas as pd

def plot_cumulative_returns(
    port_cum: pd.Series,
    bench_cum: pd.Series,
    title: str = "Cumulative Returns"
):
    fig, ax = plt.subplots()
    ax.plot(port_cum, label='Portfolio')
    ax.plot(bench_cum, label='Benchmark')
    ax.set_title(title)
    ax.legend()
    ax.set_ylabel('Cumulative Return')
    ax.set_xlabel('Date')
    plt.tight_layout()
    plt.show()

# Add more: pie chart allocation, drawdown plot, rolling Sharpe, etc.
