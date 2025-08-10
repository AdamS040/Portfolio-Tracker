import matplotlib.pyplot as plt
import pandas as pd
import os

import matplotlib.pyplot as plt
import pandas as pd

def plot_cumulative_returns(
    port_cum: pd.Series,
    bench_cum: pd.Series,
    title: str = "Cumulative Returns",
    return_fig: bool = False
):
    fig, ax = plt.subplots()
    ax.plot(port_cum, label='Portfolio')
    ax.plot(bench_cum, label='Benchmark')
    ax.set_title(title)
    ax.legend()
    ax.set_ylabel('Cumulative Return')
    ax.set_xlabel('Date')
    plt.tight_layout()
    
    if return_fig:
        return fig
    else:
        plt.show()


def plot_drawdown(cum_returns, title='Drawdown Curve', return_fig=False):
    running_max = cum_returns.cummax()
    drawdown = (cum_returns - running_max) / running_max

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(drawdown, color='red', label='Drawdown')
    ax.fill_between(drawdown.index, drawdown, 0, color='red', alpha=0.3)
    ax.set_title(title)
    ax.set_ylabel('Drawdown')
    ax.set_xlabel('Date')
    ax.legend()
    ax.grid(True)
    
    if return_fig:
        return fig
    else:
        plt.show()


def plot_rolling_volatility(returns, window=60, title=None, return_fig=False):
    rolling_vol = returns.rolling(window).std() * (252 ** 0.5)  # Annualized volatility

    if title is None:
        title = f'Rolling {window}-day Volatility'

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(rolling_vol, label=title)
    ax.set_title(title)
    ax.set_ylabel('Volatility')
    ax.set_xlabel('Date')
    ax.legend()
    ax.grid(True)

    if return_fig:
        return fig
    else:
        plt.show()
