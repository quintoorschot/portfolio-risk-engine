from src.market_data import get_price_data
from src.dataclasses.Portfolio import Portfolio
from scipy.stats import norm
import pandas as pd
import sqlite3


def _validate_confidence_level(confidence_level: float) -> None:
    "Validate if given confidence level C is within valid bounds (0 < C < 1)"

    if not 0 < confidence_level < 1:
        raise ValueError(f"[ERROR]: confidence level ({confidence_level}) should be between 0 and 1!")


def _get_historical_pnl(
        connection: sqlite3.Connection,
        portfolio: Portfolio
    ) -> pd.DataFrame:
    """Calculate hypothetical PnL for historical returns given current exposures"""

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
        confidence_level: float = 0.95
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

    historical_pnl: pd.Series = _get_historical_pnl(connection, portfolio)
    losses: pd.Series = -historical_pnl

    value_at_risk: float = float(
        losses.quantile(confidence_level, interpolation="higher")
    )

    return value_at_risk


def calculate_parametric_var(
        connection: sqlite3.Connection,
        portfolio: Portfolio,
        confidence_level: float = 0.95
    ) -> float:
    """Calculate the parametric (variance-covariance) Value at Risk (VaR) for a portfolio
    
    Assumes portfolio returns follow a normal distribution, using the historical 
    mean and volatility to estimate the maximum expected loss at a given 
    confidence level.
    
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

    historical_pnl: pd.Series = _get_historical_pnl(connection, portfolio)

    mean_pnl: float = float(historical_pnl.mean())
    pnl_volatility: float = float(historical_pnl.std(ddof=1))

    z_score: float = float(norm.ppf(confidence_level))

    value_at_risk: float = z_score * pnl_volatility - mean_pnl

    return value_at_risk