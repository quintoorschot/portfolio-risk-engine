from scipy.stats import norm
import pandas as pd
import numpy as np

def calculate_historical_cvar(
    daily_pnl: pd.Series,
    confidence_level: float = 0.95,
    horizon_days: int = 1,
) -> float:
    """Calculate historical Conditional Value at Risk (CVaR)."""

    _validate_confidence_level(confidence_level)
    _validate_horizon_days(horizon_days)
    _validate_pnl_length(daily_pnl, horizon_days)

    if len(daily_pnl) < horizon_days:
        raise ValueError(f"[ERROR]: Not enough observations to calculate historical VaR! The number of observations ({len(daily_pnl)}) should be larger than the value of horizon days ({horizon_days})!")

    horizon_pnl: pd.Series = pd.Series(
        daily_pnl
        .rolling(window=horizon_days)
        .sum()
        .dropna()
    )

    if horizon_pnl.empty:
        raise ValueError("[ERROR]: Not enough historical PnL data to calculate CVaR!")

    var_threshold: float = horizon_pnl.quantile(
        1 - confidence_level
    )

    tail_losses: pd.Series = horizon_pnl[horizon_pnl <= var_threshold]

    if tail_losses.empty:
        raise ValueError("[ERROR]: No valid observations for CVaR!")

    cvar: float = -float(tail_losses.mean())

    return max(cvar, 0.0)


def calculate_parametric_cvar(
    daily_pnl: pd.Series,
    confidence_level: float = 0.95,
    horizon_days: int = 1,
) -> float:
    """Calculate parametric (variance-covariance) Conditional Value at Risk (CVaR)."""

    _validate_confidence_level(confidence_level)
    _validate_horizon_days(horizon_days)
    _validate_pnl_length(daily_pnl, 1)

    daily_pnl_mean: float = daily_pnl.mean()
    daily_pnl_volatility: float = daily_pnl.std()

    horizon_mean: float = daily_pnl_mean * horizon_days
    horizon_volatility: float = daily_pnl_volatility * np.sqrt(horizon_days)

    z_score: float = float(norm.ppf(1 - confidence_level))
    tail_probability: float = float(norm.cdf(z_score))

    cvar = (
        horizon_volatility * norm.pdf(z_score) / tail_probability
        - horizon_mean
    )

    return max(float(cvar), 0.0)


def _validate_confidence_level(
    confidence_level: float,
) -> None:
    if not 0 < confidence_level < 1:
        raise ValueError(f"[ERROR]: Confidence level c ({confidence_level}) should be in a valid range (i.e. 0 < c < 1)!")

def _validate_horizon_days(
    horizon_days: int,
) -> None:
    if not isinstance(horizon_days, int) or horizon_days < 1:
        raise ValueError(f"[ERROR]: Horizon days ({horizon_days}) should be a postive integer")

def _validate_pnl_length(
    daily_pnl: pd.Series,
    minimum_length: int,
) -> None:
    if len(daily_pnl) < minimum_length:
        raise ValueError(f"[ERROR]: Not enough observations to calculate VaR! The number of observations ({len(daily_pnl)}) is too small!")