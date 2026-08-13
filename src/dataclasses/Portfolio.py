from dataclasses import dataclass, field
from src.dataclasses.Position import Position
from src.market_data import get_price_data
from collections.abc import Iterator
from typing import List, Any
import pandas as pd
import numpy as np
import sqlite3

from src.var import calculate_historical_var, calculate_parametric_var
from src.cvar import calculate_historical_cvar, calculate_parametric_cvar

@dataclass(repr=False)
class Portfolio:
    """Represents an investment portfolio with positions and risk calculations."""

    connection: sqlite3.Connection
    portfolio_id: str

    portfolio_name: str = field(init=False)
    base_currency: str = field(init=False)
    positions: List[Position] = field(default_factory=list)
    total_value: float = field(init=False)

    def __post_init__(self) -> None:
        query: str = """
            SELECT portfolio_name, base_currency
            FROM portfolios
            WHERE portfolio_id = ?
        """
        self.portfolio_name, self.base_currency = pd.read_sql_query(query, self.connection, params=(self.portfolio_id,)).iloc[0]
        self.positions = self._fetch_positions()
        self.total_value = np.sum([position.market_price for position in self.positions])


    def __iter__(self) -> Iterator[Position]:
        return iter(self.positions)


    def __repr__(self) -> str:
        seperator: str = "=" * 70
        positions: str = '\n'.join(f"\t{p.instrument_id}: {p.quantity} × ${p.market_price}" for p in self.positions)

        return (
            f"Portfolio {self.portfolio_id} ({self.base_currency}):\n"
            f"{seperator}\n"
            f"TOTAL VALUE: ${self.total_value}\n"
            f"POSITIONS:\n"
            f"{positions}\n\n"
            f"{seperator}\n"
            f"VALUE-AT-RISK:\n"
            f"\tDaily historical VaR (95% confidence): ${self.historical_var():.2f}\n"
            f"\tDaily parametric VaR (95% confidence): ${self.parametric_var():.2f}\n\n"
            f"{seperator}\n"
            f"CONDITIONAL VALUE-AT-RISK:\n"
            f"\tDaily historical CVaR (95% confidence): ${self.historical_cvar():.2f}\n"
            f"\tDaily parametric CVaR (95% confidence): ${self.parametric_cvar():.2f}\n\n"
        )


    def historical_var(self, confidence_level: float = 0.95, horizon_days: int = 1) -> float:
        """Calculate the historical Value at Risk (VaR) for the portfolio.

        Uses historical portfolio PnL observations to estimate the maximum expected
        loss at a given confidence level over the specified holding period.

        Args:
            confidence_level: Confidence level for the VaR calculation. Must satisfy
                0 < confidence_level < 1. Defaults to 0.95.
            horizon_days: Number of trading days over which to calculate VaR. Must be
                a positive integer. Defaults to 1.

        Returns:
            The estimated maximum portfolio loss (>= 0.0) at the given confidence
            level.

        Raises:
            ValueError: If the confidence level is invalid, the horizon is invalid,
                or there is insufficient historical price data to calculate VaR.
        """
        return calculate_historical_var(
            daily_pnl = self._get_historical_pnl(self.connection),
            confidence_level = confidence_level,
            horizon_days = horizon_days
        )


    def parametric_var(self, confidence_level: float = 0.95, horizon_days: int = 1) -> float:
        """Calculate the parametric (variance-covariance) Value at Risk (VaR) for the portfolio.

        Uses the historical portfolio PnL distribution to estimate the VaR under the
        assumption that returns are sampled from a normal distribution. The calculation is
        based on the estimated portfolio mean return and volatility over the
        specified holding period.

        Args:
            confidence_level: Confidence level for the VaR calculation. Must satisfy
                0 < confidence_level < 1. Defaults to 0.95.
            horizon_days: Number of trading days over which to calculate VaR. Must be
                a positive integer. Defaults to 1.

        Returns:
            The estimated maximum portfolio loss (>= 0.0) at the given confidence
            level.

        Raises:
            ValueError: If the confidence level is invalid, the horizon is invalid,
                or there is insufficient historical price data to estimate portfolio
                volatility.
        """
        return calculate_parametric_var(
            self._get_historical_pnl(self.connection),
            confidence_level,
            horizon_days
        )


    def historical_cvar(self, confidence_level: float = 0.95, horizon_days: int = 1) -> float:
        """Calculate the historical Conditional Value at Risk (CVaR) for PnL data.

        Uses historical PnL observations to estimate the expected loss in the worst
        cases beyond the Value at Risk (VaR) threshold. CVaR (or Expected
        Shortfall) measures the average loss in the tail of the historical PnL
        distribution at a given confidence level.

        Args:
            daily_pnl: Series of historical daily profit-and-loss observations.
            confidence_level: Confidence level for the CVaR calculation. Must satisfy
                0 < confidence_level < 1. Defaults to 0.95.
            horizon_days: Number of trading days over which to calculate CVaR. Must be
                a positive integer. Defaults to 1.

        Returns:
            The estimated expected loss beyond the VaR threshold (>= 0.0) at the
            given confidence level.

        Raises:
            ValueError: If the confidence level is invalid, if there are insufficient
                historical PnL observations to calculate CVaR, or if no valid tail
                loss observations are available.
        """
        return calculate_historical_cvar(
            self._get_historical_pnl(self.connection),
            confidence_level,
            horizon_days
        )


    def parametric_cvar(self, confidence_level: float = 0.95, horizon: int = 1) -> float:
        """Calculate the parametric Conditional Value at Risk (CVaR) for PnL data.

        Uses a parametric model of the PnL distribution to estimate the expected loss
        in the tail beyond the Value at Risk (VaR) threshold. Unlike historical CVaR,
        which relies directly on observed PnL scenarios, parametric CVaR assumes a
        statistical distribution for returns (e.g., normal distribution) and derives
        the tail loss analytically based on the estimated distribution parameters.

        CVaR (or Expected Shortfall) measures the average loss in the worst cases
        beyond the VaR threshold at a given confidence level.

        Args:
            daily_pnl: Series of historical daily profit-and-loss observations used to
                estimate the distribution parameters (e.g., mean and volatility).
            confidence_level: Confidence level for the CVaR calculation. Must satisfy
                0 < confidence_level < 1. Defaults to 0.95.
            horizon_days: Number of trading days over which to calculate CVaR. Must be
                a positive integer. Defaults to 1.

        Returns:
            The estimated expected loss beyond the VaR threshold (>= 0.0) at the given
            confidence level under the assumed parametric distribution.

        Raises:
            ValueError: If the confidence level is invalid, if the time horizon is
                invalid, if there are insufficient PnL observations to estimate the
                distribution parameters, or if the parametric calculation cannot
                produce a valid CVaR estimate.
        """
        return calculate_parametric_cvar(
            self._get_historical_pnl(self.connection),
            confidence_level,
            horizon,
        )



    def _fetch_positions(self) -> List[Position]:
        """Fetches a portfolio's position data from the database and stores it in the portfolio instance"""

        query: str = """
            SELECT position_id, instrument_id, quantity, market_price
            FROM positions
            WHERE portfolio_id = ?
        """
        cursor: sqlite3.Cursor = self.connection.execute(query, (self.portfolio_id,))
        rows: List[Any] = cursor.fetchall()

        return [
            Position(
                portfolio_id = self.portfolio_id,
                position_id = row[0],
                instrument_id=row[1],
                quantity=row[2],
                market_price=row[3]
            )
            for row in rows
        ]


    def _get_historical_pnl(self, connection: sqlite3.Connection) -> pd.Series:
        """Calculates the portfolio's historical PnL by applying current position exposures to historical asset returns derived from price data."""

        # Get price history of all assets in portfolio
        prices: pd.DataFrame = get_price_data(connection, [position.instrument_id for position in self])

        # Calculate daily returns by taking the percentage returns between days
        returns: pd.DataFrame = prices.pct_change().dropna()

        # Current exposure for asset = asset quantity × asset market price
        current_exposures = pd.Series(
            {
                position.instrument_id: position.quantity * position.market_price
                for position in self
            },
            dtype=float
        )

        if len(prices) < 2:
            raise ValueError("[ERROR]: Not enough price history to calculate VaR!")

        # Calculate PnL for each asset on every day
        # For each day we calculate: PnL day i = return day i * current exposures
        return (
            returns
            .mul(current_exposures, axis="columns")
            .sum(axis="columns")
        )