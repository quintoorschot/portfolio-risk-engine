from src.market_data import get_price_data
from src.dataclasses.Portfolio import Portfolio
from scipy.stats import norm
from typing import List, Tuple
import pandas as pd
import numpy as np
import sqlite3


def _validate_confidence_interval(confidence_interval: float) -> None:

    if not 0 < confidence_interval < 1:
        raise ValueError(f"[ERROR]: confidence interval ({confidence_interval}) should be between 0 and 1!")


def _prepare_var_data(connection: sqlite3.Connection, portfolio: Portfolio) -> Tuple[pd.Series, float]:

    quantities = pd.Series(
        {
            position.instrument_id: position.quantity
            for position in portfolio
        },
        dtype=float,
    )

    prices: pd.DataFrame = (
        pd.concat(
            (
                get_price_data(connection, position.instrument_id)
                for position in portfolio
            ),
            ignore_index=True,
        )
        .pivot(
            index='price_date',
            columns='instrument_id',
            values='market_price',
        )
        .reindex(columns=quantities.index).dropna()
    )

    if len(prices) < 2:
        raise ValueError("[ERROR] Not enough price history to calculate VaR!")

    historical_total_values: pd.Series = prices.mul(quantities, axis="columns").sum(axis=1)
    returns: pd.Series = historical_total_values.apply(np.log).diff().dropna()

    if returns.empty:
        raise ValueError("Not enough returns to calculate VaR")

    current_portfolio_value: float = sum(
        position.market_price * position.quantity
        for position in portfolio
    )

    return returns, current_portfolio_value



def calculate_historical_var(
        connection: sqlite3.Connection,
        portfolio: Portfolio,
        confidence_interval: float = 0.95
    ) -> float:
    """Calculate the historical Value at Risk (VaR) for a portfolio
    
    Uses historical portfolio returns to estimate the maximum expected loss at a given confidence level over the historical period.
    
    Args:
        connection: Active SQLite database connection containing historical price data.
        portfolio: Portfolio object containing assets and weights.
        confidence_interval: Confidence level (0 < c < 1) for the calculation. Defaults to 0.95.

    Returns:
        The estimated maximum loss (>= 0.0) at the given confidence level.

    Raises:
        ValueError: If the confidence interval is invalid or if there are insufficient historical returns to compute VaR.
    """

    _validate_confidence_interval(confidence_interval)

    quantities = pd.Series(
        {
            position.instrument_id: position.quantity
            for position in portfolio
        },
        dtype=float,
    )

    prices: pd.DataFrame = (
        pd.concat(
            (
                get_price_data(connection, position.instrument_id)
                for position in portfolio
            ),
            ignore_index=True,
        )
        .pivot(
            index='price_date',
            columns='instrument_id',
            values='market_price',
        )
        .reindex(columns=quantities.index).dropna()
    )

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

    scenario_pnl: pd.Series = returns.mul(current_exposures, axis="columns").sum(axis=1)
    losses: pd.Series = -scenario_pnl

    value_at_risk: float = float(
        losses.quantile(confidence_interval, interpolation="higher")
    )

    return value_at_risk


def calculate_parametric_var(
        connection: sqlite3.Connection,
        portfolio: Portfolio,
        confidence_interval: float = 0.95
    ) -> float:
    """Calculate the parametric (variance-covariance) Value at Risk (VaR) for a portfolio
    
    Assumes portfolio returns follow a normal distribution, using the historical 
    mean and volatility to estimate the maximum expected loss at a given 
    confidence level.
    
    Args:
        connection: Active SQLite database connection containing historical price data.
        portfolio: Portfolio object containing assets and weights.
        confidence_interval: Confidence level (0 < c < 1) for the calculation. Defaults to 0.95.

    Returns:
        The estimated maximum loss (>= 0.0) at the given confidence level.

    Raises:
        ValueError: If the confidence interval is invalid or if there are insufficient historical returns to compute VaR.
    """

    _validate_confidence_interval(confidence_interval)

    returns, current_portfolio_value = _prepare_var_data(connection, portfolio)
    mean_return, volatility = returns.mean(), returns.std()

    current_portfolio_value: float = sum(
        position.market_price * position.quantity
        for position in portfolio
    )

    z_index: float = float(norm.ppf(confidence_interval))
    value_at_risk: float = current_portfolio_value * (z_index * volatility - mean_return)

    return value_at_risk