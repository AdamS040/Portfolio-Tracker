# src/visualization.py
import matplotlib.pyplot as plt
import pandas as pd


def plot_cumulative_returns(
    port_cum: pd.Series,
    bench_cum: pd.Series,
    title: str = "Cumulative Returns",
    return_fig: bool = False,
):
    fig, ax = plt.subplots()
    ax.plot(port_cum, label="Portfolio")
    ax.plot(bench_cum, label="Benchmark")
    ax.set_title(title)
    ax.set_ylabel("Cumulative Return")
    ax.set_xlabel("Date")
    ax.legend()
    ax.tick_params(axis="x", labelsize=8)
    plt.tight_layout()

    if return_fig:
        return fig
    else:
        plt.show()


def plot_drawdown(
    cum_returns: pd.Series,
    title: str = "Drawdown Curve",
    return_fig: bool = False,
):
    running_max = cum_returns.cummax()
    drawdown = (cum_returns - running_max) / running_max

    fig, ax = plt.subplots()
    ax.plot(drawdown, label="Drawdown")
    ax.fill_between(drawdown.index, drawdown, 0, alpha=0.3)
    ax.set_title(title)
    ax.set_ylabel("Drawdown")
    ax.set_xlabel("Date")
    ax.legend()
    ax.grid(True)

    if return_fig:
        return fig
    else:
        plt.show()


def plot_rolling_volatility(
    returns: pd.Series,
    window: int = 60,
    title: str | None = None,
    return_fig: bool = False,
):
    rolling_vol = returns.rolling(window).std() * (252 ** 0.5)  # annualized

    if title is None:
        title = f"Rolling {window}-day Volatility"

    fig, ax = plt.subplots()
    ax.plot(rolling_vol, label=title)
    ax.set_title(title)
    ax.set_ylabel("Volatility")
    ax.set_xlabel("Date")
    ax.legend()
    ax.grid(True)

    if return_fig:
        return fig
    else:
        plt.show()
