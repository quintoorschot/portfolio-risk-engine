from src.market_data import get_price_data
from src.dataclasses.Portfolio import Portfolio
from scipy.stats import norm
import pandas as pd
import numpy as np
import sqlite3


def _validate_confidence_level(confidence_level: float) -> None:
    "Validate if given confidence level C is within valid bounds (0 < C < 1)"

    if not 0 < confidence_level < 1:
        raise ValueError(f"[ERROR]: confidence level ({confidence_level}) should be between 0 and 1!")


def _get_historical_pnl(
        connection: sqlite3.Connection,
        portfolio: Portfolio
    ) -> pd.DataFrame:
    """Calculate hypothetical daily PnL for historical returns given current exposures"""

    prices: pd.DataFrame = get_price_data(connection, [position.instrument_id for position in portfolio])

    if len(prices) < 2:
        raise ValueError("[ERROR] Not enough price history to calculate VaR!")

    returns: pd.DataFrame = prices.pct_change().dropna()
    current_exposures: pd.Series = pd.Series(
        {
            position.instrument_id: position.quantity * position.market_price
            for position in portfolio
        },
        dtype=float,
    )

    historical_pnl: pd.Series = returns.mul(current_exposures, axis="columns").sum(axis=1)

    return historical_pnl


def calculate_historical_var(
        connection: sqlite3.Connection,
        portfolio: Portfolio,
        confidence_level: float = 0.95,
        horizon_days: int = 1
    ) -> float:
    """Calculate the historical Value at Risk (VaR) for a portfolio
    
    Uses historical portfolio returns to estimate the maximum expected loss at a given confidence level over the historical period.
    
    Args:
        connection: Active SQLite database connection containing historical price data.
        portfolio: Portfolio object containing assets and weights.
        confidence_level: Confidence level (0 < c < 1) for the calculation. Defaults to 0.95.

    Returns:
        The estimated maximum loss (>= 0.0) at the given confidence level.

    Raises:
        ValueError: If the confidence level is invalid or if there are insufficient historical returns to compute VaR.
    """

    _validate_confidence_level(confidence_level)

    daily_pnl: pd.Series = _get_historical_pnl(connection, portfolio)

    historical_pnl: pd.Series = (
        daily_pnl
        .rolling(window=horizon_days)
        .sum()
        .dropna()
    )

    losses: pd.Series = -historical_pnl

    value_at_risk: float = float(
        losses.quantile(confidence_level, interpolation="higher")
    )

    return value_at_risk


def calculate_parametric_var(
        connection: sqlite3.Connection,
        portfolio: Portfolio,
        confidence_level: float = 0.95,
        horizon_days: int = 1
    ) -> float:
    """Calculate the parametric (variance-covariance) Value at Risk (VaR) for a portfolio
    
    Assumes portfolio returns follow a normal distribution, using the historical 
    mean and volatility to estimate the maximum expected loss at a given 
    confidence level.
    
    Args:
        connection: Active SQLite database connection containing historical price data.
        portfolio: Portfolio object containing assets and weights.
        confidence_level: Confidence level (0 < c < 1) for the calculation. Defaults to 0.95.
        horizon_days: number of trading days over which we calculate the VaR.

    Returns:
        The estimated maximum loss (>= 0.0) at the given confidence level.

    Raises:
        ValueError: If the confidence level is invalid or if there are insufficient historical returns to compute VaR.
    """

    _validate_confidence_level(confidence_level)

    daily_pnl: pd.Series = _get_historical_pnl(connection, portfolio)

    mean_daily_pnl: float = float(daily_pnl.mean())
    pnl_daily_volatility: float = float(daily_pnl.std(ddof=1))

    z_score: float = float(norm.ppf(confidence_level))

    daily_value_at_risk: float = z_score * pnl_daily_volatility - mean_daily_pnl

    value_at_risk: float = daily_value_at_risk * np.sqrt(horizon_days)

    return value_at_risk