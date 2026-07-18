from dataclasses import dataclass, field
from src.dataclasses.Returns import Returns
from src.var import calculate_historical_var
from src.market_data import get_price_data
import pandas as pd
import sqlite3

@dataclass
class Portfolio:

    connection: sqlite3.Connection
    portfolio_id: str

    portfolio_name: str = field(init=False)
    base_currency: str = field(init=False)
    positions: pd.DataFrame = field(default_factory=pd.DataFrame)

    def __post_init__(self) -> None:
        query: str = """
            SELECT portfolio_name, base_currency
            FROM portfolios
            WHERE portfolio_id = ?
        """
        result: pd.DataFrame = pd.read_sql_query(query, self.connection, params=(self.portfolio_id,))
        self.portfolio_name, self.base_currency = result.iloc[0]
        self._fetch_positions()
        self.positions['total_position_value'] = self.positions['quantity'] * self.positions['market_price']


    def historical_var(self, confidence_interval: float = 0.95) -> float:
        """Takes a confidence interval between 0 and 1 and calculates historical value-at-risk"""

        if not 0 <= confidence_interval <= 1:
            raise ValueError("[ERROR]: Confidence interval must be in range [0, 1]!")

        total_value_at_risk: float = 0
        for position in self.positions.itertuples():

            if not isinstance(position.total_position_value, float):
                raise TypeError("[ERROR]: total_position_value is expected to by of type float!")
            
            total_position_value: float = float(position.total_position_value)
            price_history: pd.DataFrame = get_price_data(self.connection, str(position.instrument_id))
            returns: Returns = Returns(price_history)
            total_value_at_risk += calculate_historical_var(total_position_value, returns, confidence_interval)

        return total_value_at_risk


    def _fetch_positions(self) -> None:
        """Fetches the position data from the database and stores it in the portfolio instance"""

        query: str = """
            SELECT position_id, instrument_id, quantity, market_price
            FROM positions
            WHERE portfolio_id = ?
        """
        self.positions = pd.read_sql_query(query, self.connection, params=(self.portfolio_id,))