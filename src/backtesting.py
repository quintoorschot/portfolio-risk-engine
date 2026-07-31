from src.dataclasses.Portfolio import Portfolio
from src.dataclasses.VaRBacktestResult import VaRBacktestObservation, VaRBacktestSummary
from src.market_data import get_price_data
from src.var import calculate_historical_var
from sqlite3 import Connection
import pandas as pd

def backtest_historical_var(
        connection: Connection,
        portfolio: Portfolio,
        confidence_level: float = 0.95,
        window: int = 250,
    ) -> VaRBacktestSummary:
    """One-day historical VaR backtest."""

    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be between 0 and 1")

    if window < 2:
        raise ValueError("window must be at least 2")

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
    backtest_summary: VaRBacktestSummary = None
    for i in range(window + 1, len(prices)):
        historical_returns: pd.DataFrame = returns.iloc[i - window:i].dropna()

        previous_prices: pd.Series = prices.iloc[i - 1]
        current_prices: pd.Series = prices.iloc[i]

        exposures: pd.Series = quantities * previous_prices
        historical_pnl: pd.Series = historical_returns.mul(exposures, axis="columns").sum(axis="columns")

        value_at_risk: float = calculate_historical_var(
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

    backtest_summary: VaRBacktestSummary = VaRBacktestSummary(result, confidence_level)

    return backtest_summary
