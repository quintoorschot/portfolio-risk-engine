from scipy.stats import norm
import pandas as pd
import numpy as np

def calculate_historical_var(
        daily_pnl: pd.Series,
        confidence_level: float = 0.95,
        horizon_days: int = 1,
    ) -> float:
    """Calculate the historical Value at Risk (VaR) for P&L data
    
    Uses historical P&L data to estimate the maximum expected loss at a given confidence level over the historical period.
    
    Args:
        daily_pnl: Series of historical daily profit-and-loss observations.
        confidence_level: Confidence level for the VaR calculation. Must satisfy 0 < confidence_level < 1. Defaults to 0.95.
        horizon_days: Number of trading days over which to calculate VaR. Must be a positive integer. Defaults to 1.

    Returns:
        The estimated maximum loss (>= 0.0) at the given confidence level.

    Raises:
        ValueError: If the confidence level is invalid or if there are insufficient historical returns to compute VaR.
    """

    if not 0 < confidence_level < 1:
        raise ValueError("[ERROR]: confidence level should be in a valid range (i.e. 0 < c < 1)!")

    horizon_pnl: pd.Series = daily_pnl.rolling(window=horizon_days).sum().dropna()

    value_at_risk: float = -float(horizon_pnl.quantile(1 - confidence_level))
    value_at_risk = max(value_at_risk, 0.0)

    return value_at_risk


def calculate_parametric_var(
        daily_pnl: pd.Series,
        confidence_level: float = 0.95,
        horizon_days: int = 1,
    ) -> float:
    """Calculate the parametric (variance-covariance) Value at Risk (VaR) for a portfolio
    
    Assumes portfolio returns follow a normal distribution, using the historical 
    mean and volatility to estimate the maximum expected loss at a given 
    confidence level.
    
    Args:
        daily_pnl: Series of historical daily profit-and-loss observations.
        confidence_level: Confidence level for the VaR calculation. Must satisfy 0 < confidence_level < 1. Defaults to 0.95.
        horizon_days: Number of trading days over which to calculate VaR. Must be a positive integer. Defaults to 1.

    Returns:
        The estimated maximum loss (>= 0.0) at the given confidence level.

    Raises:
        ValueError: If the confidence level is invalid or if there are insufficient historical returns to compute VaR.
    """

    if not 0 < confidence_level < 1:
        raise ValueError("[ERROR]: confidence level should be in a valid range (i.e. 0 < c < 1)!")

    daily_pnl_mean: float = daily_pnl.mean()
    daily_pnl_volatility: float = daily_pnl.std()

    z_score: float = float(norm.ppf(confidence_level))

    value_at_risk: float = z_score * np.sqrt(horizon_days) * daily_pnl_volatility - daily_pnl_mean * horizon_days

    return value_at_risk