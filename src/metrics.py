import numpy as np
import pandas as pd
import scipy as scipy
from scipy import stats
from typing import Dict


def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float,
    freq: int = 252
) -> float:
    """Annualized Sharpe ratio."""
    excess = returns - risk_free_rate / freq
    return np.sqrt(freq) * excess.mean() / excess.std()

def max_drawdown(returns: pd.Series) -> float:
    """Maximum peak-to-trough drawdown."""
    cum = (1 + returns).cumprod()
    peak = cum.cummax()
    drawdown = (cum - peak) / peak
    return drawdown.min()

def alpha_beta(
    port_returns: pd.Series,
    bench_returns: pd.Series,
    risk_free_rate: float = 0.01,
    freq: int = 252
) -> Dict[str, float]:
    """Calculate annualized alpha and beta via linear regression of excess returns."""

    # Convert annual risk-free rate to per-period (assuming returns frequency matches freq)
    rf_per_period = risk_free_rate / freq

    # Calculate excess returns by subtracting risk-free rate per period
    excess_p = port_returns - rf_per_period
    excess_b = bench_returns - rf_per_period

    beta, alpha, r_val, p_val, std_err = stats.linregress(excess_b, excess_p)

    # Annualize alpha by multiplying intercept by freq
    alpha_annualized = alpha * freq

    return {'alpha': alpha_annualized, 'beta': beta}
