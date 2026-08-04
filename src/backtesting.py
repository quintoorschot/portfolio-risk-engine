from src.dataclasses.Portfolio import Portfolio
from src.dataclasses.VaRBacktestResult import VaRBacktestObservation, VaRBacktestSummary
from src.market_data import get_price_data
from src.var import calculate_historical_var, calculate_parametric_var
from sqlite3 import Connection
import pandas as pd

def backtest_historical_var(
        connection: Connection,
        portfolio: Portfolio,
        confidence_level: float = 0.95,
        window: int = 250,
        horizon_days: int = 1,
    ) -> VaRBacktestSummary:
    """Historical VaR backtest."""

    if not 0 < confidence_level < 1:
        raise ValueError(f"[ERROR]: Confidence_level ({confidence_level}) must be between 0 and 1!")

    if window < 2:
        raise ValueError(f"[ERROR]: Window ({window}) must be at least 2!")

    if horizon_days < 1:
        raise ValueError(f"[ERROR]: Horizon_days ({horizon_days}) must be a non-negative integer!")

    quantities: pd.Series = pd.Series(
        {
            position.instrument_id: position.quantity
            for position in portfolio
        }
    )

    prices: pd.DataFrame = get_price_data(
        connection,
        quantities.index.tolist(),
    )
    returns: pd.DataFrame = prices.pct_change()

    result = []
    for i in range(window + 1, len(prices) - horizon_days + 1):
        historical_returns: pd.DataFrame = returns.iloc[i - window:i].dropna()

        previous_prices: pd.Series = prices.iloc[i - 1]
        future_prices: pd.Series = prices.iloc[i + horizon_days - 1]

        exposures: pd.Series = quantities * previous_prices
        historical_pnl: pd.Series = historical_returns.mul(exposures, axis="columns").sum(axis="columns")

        value_at_risk: float = calculate_historical_var(
            historical_pnl,
            confidence_level,
            horizon_days,
        )
        actual_pnl: float = ((future_prices - previous_prices) * quantities).sum()

        exception: bool = actual_pnl < -value_at_risk

        result.append(
            VaRBacktestObservation(
                prices.index[i],
                value_at_risk,
                actual_pnl,
                exception,
            )
        )

    return VaRBacktestSummary(result, confidence_level)


def backtest_parametric_var(
        connection: Connection,
        portfolio: Portfolio,
        confidence_level: float = 0.95,
        window: int = 250,
    ) -> VaRBacktestSummary:
    """One-day parametric (variance-covariance) VaR backtest."""

    if not 0 < confidence_level < 1:
        raise ValueError(f"[ERROR]: Confidence_level ({confidence_level}) must be between 0 and 1!")

    if window < 2:
        raise ValueError(f"[ERROR]: Window ({window}) must be at least 2!")

    quantities: pd.Series = pd.Series(
        {
            position.instrument_id: position.quantity
            for position in portfolio
        }
    )

    prices: pd.DataFrame = get_price_data(
        connection,
        quantities.index.tolist(),
    )
    returns: pd.DataFrame = prices.pct_change()

    result = []
    for i in range(window + 1, len(prices)):
        historical_returns: pd.DataFrame = returns.iloc[i - window:i].dropna()

        previous_prices: pd.Series = prices.iloc[i - 1]
        current_prices: pd.Series = prices.iloc[i]

        exposures: pd.Series = quantities * previous_prices
        historical_pnl: pd.Series = historical_returns.mul(exposures, axis="columns").sum(axis="columns")

        value_at_risk: float = calculate_parametric_var(
            historical_pnl,
            confidence_level
        )
        actual_pnl: float = ((current_prices - previous_prices) * quantities).sum()

        exception: bool = actual_pnl < -value_at_risk

        result.append(
            VaRBacktestObservation(
                prices.index[i],
                value_at_risk,
                actual_pnl,
                exception,
            )
        )

    return VaRBacktestSummary(result, confidence_level)
