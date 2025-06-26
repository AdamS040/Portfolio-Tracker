import numpy as np
import pandas as pd
from scipy import stats

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
    freq: int = 252
) -> Dict[str, float]:
    """Linear regression of excess returns to get alpha & beta."""
    excess_p = port_returns - port_returns.mean()
    excess_b = bench_returns - bench_returns.mean()
    beta, alpha, r_val, p_val, std_err = stats.linregress(excess_b, excess_p)
    return {'alpha': alpha * freq, 'beta': beta}
