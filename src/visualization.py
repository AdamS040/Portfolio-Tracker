import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_cumulative_returns(
    port_cum: pd.Series,
    bench_cum: pd.Series,
    title: str = "Cumulative Returns",
    save_path: str = None
):
    fig, ax = plt.subplots()
    ax.plot(port_cum, label='Portfolio')
    ax.plot(bench_cum, label='Benchmark')
    ax.set_title(title)
    ax.legend()
    ax.set_ylabel('Cumulative Return')
    ax.set_xlabel('Date')
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
    plt.show()
    plt.close()


def plot_drawdown(cum_returns, save_path=None):
    """
    Plot the drawdown curve of cumulative returns.

    cum_returns: pd.Series or pd.DataFrame with cumulative returns (e.g. (1+returns).cumprod())
    save_path: optional file path to save the plot
    """
    running_max = cum_returns.cummax()
    drawdown = (cum_returns - running_max) / running_max

    plt.figure(figsize=(10, 6))
    plt.plot(drawdown, color='red', label='Drawdown')
    plt.fill_between(drawdown.index, drawdown, 0, color='red', alpha=0.3)
    plt.title('Drawdown Curve')
    plt.ylabel('Drawdown')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True)
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
    plt.show()
    plt.close()


def plot_rolling_volatility(returns, window=60, save_path=None):
    """
    Plot rolling volatility of returns.

    returns: pd.Series or pd.DataFrame with periodic returns
    window: rolling window size in days
    save_path: optional file path to save the plot
    """
    rolling_vol = returns.rolling(window).std() * (252**0.5)  # Annualized volatility

    plt.figure(figsize=(10, 6))
    plt.plot(rolling_vol, label=f'Rolling {window}-day Volatility')
    plt.title(f'Rolling {window}-day Volatility')
    plt.ylabel('Volatility')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True)
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
    plt.show()
    plt.close()
