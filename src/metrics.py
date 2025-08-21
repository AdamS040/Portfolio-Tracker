# src/metrics.py
from typing import Dict

import numpy as np
import pandas as pd
from scipy import stats


def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float,
    freq: int = 252,
) -> float:
    """Annualized Sharpe ratio."""
    rf_per_period = risk_free_rate / freq
    excess = returns - rf_per_period
    denom = excess.std()
    if denom == 0 or np.isnan(denom):
        return float("nan")
    return np.sqrt(freq) * excess.mean() / denom


def max_drawdown(returns: pd.Series) -> float:
    """Maximum peak-to-trough drawdown (negative number)."""
    cum = (1 + returns).cumprod()
    peak = cum.cummax()
    drawdown = (cum - peak) / peak
    return float(drawdown.min())


def alpha_beta(
    port_returns: pd.Series,
    bench_returns: pd.Series,
    risk_free_rate: float = 0.01,
    freq: int = 252,
) -> Dict[str, float]:
    """
    Calculate annualized alpha and beta via linear regression of EXCESS returns.
    Returns:
        {'alpha': float (annualized), 'beta': float}
    """
    rf_per_period = risk_free_rate / freq

    excess_p = port_returns - rf_per_period
    excess_b = bench_returns - rf_per_period

    # Align indices
    aligned = pd.concat([excess_p, excess_b], axis=1).dropna()
    if aligned.shape[0] < 2:
        return {"alpha": float("nan"), "beta": float("nan")}

    y = aligned.iloc[:, 0]
    x = aligned.iloc[:, 1]

    beta, alpha, r_val, p_val, std_err = stats.linregress(x, y)

    alpha_annualized = alpha * freq
    return {"alpha": float(alpha_annualized), "beta": float(beta)}
