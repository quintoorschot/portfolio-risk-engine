from src.market_data import get_price_data
from src.dataclasses.Portfolio import Portfolio
from scipy.stats import norm
from typing import List
import pandas as pd
import numpy as np
import sqlite3

def calculate_historical_var(connection: sqlite3.Connection, portfolio: Portfolio, confidence_interval: float = 0.95) -> float:

    if not 0 < confidence_interval < 1:
        raise ValueError(f"[ERROR]: confidence interval {confidence_interval} should be between 0 and 1!")

    positions: List = list(portfolio)

    price_data: List[pd.DataFrame] = [get_price_data(connection, position.instrument_id) for position in portfolio]

    combined: pd.DataFrame = pd.concat(price_data, ignore_index=True)

    wide: pd.DataFrame = combined.pivot(
        index='price_date',
        columns='instrument_id',
        values='market_price',
    )

    quantities = pd.Series(
        {
            position.instrument_id: position.quantity
            for position in portfolio
        },
        dtype=float,
    )

    wide = wide.reindex(columns=quantities.index)

    wide = wide.dropna()

    if len(wide) < 2:
        raise ValueError("[ERROR] Not enough price history to calculate VaR!")

    historical_values: pd.Series = wide.mul(quantities, axis="columns").sum(axis=1)
    returns: pd.Series = historical_values.apply(np.log).diff().dropna()

    if returns.empty:
        raise ValueError("Not enough returns to calculate VaR")

    return_at_risk: float = float(returns.quantile(1 - confidence_interval, interpolation="lower"))

    current_portfolio_value: float = sum(
        position.market_price * position.quantity
        for position in positions
    )

    value_at_risk: float = max(0.0, -current_portfolio_value * return_at_risk)

    return value_at_risk


# def calculate_parametric_var(position_value: float, returns: Returns, confidence_interval: float = 0.95) -> float:

#     if position_value < 0:
#         raise ValueError(f"[ERROR]: Position value ({position_value}) must be non-negative!")
    
#     if not 0 < confidence_interval < 1:
#         raise ValueError(f"[ERROR]: Confidence interval ({confidence_interval}) must be between 0 and 1!")

#     returns_mean: float = np.mean(returns.log_returns)
#     returns_std:  float = np.std(returns.log_returns)

#     z_value: float = float(norm.ppf(confidence_interval))

#     value_at_risk: float = position_value * ((z_value * returns_std) - returns_mean)
#     return value_at_risk