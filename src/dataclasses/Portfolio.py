from dataclasses import dataclass, field
from src.dataclasses.Position import Position
from src.market_data import get_price_data
from collections.abc import Iterator
from typing import List, Any
import pandas as pd
import sqlite3

@dataclass
class Portfolio:

    connection: sqlite3.Connection
    portfolio_id: str

    portfolio_name: str = field(init=False)
    base_currency: str = field(init=False)
    positions: List[Position] = field(default_factory=list)

    def __post_init__(self) -> None:
        query: str = """
            SELECT portfolio_name, base_currency
            FROM portfolios
            WHERE portfolio_id = ?
        """
        self.portfolio_name, self.base_currency = pd.read_sql_query(query, self.connection, params=(self.portfolio_id,)).iloc[0]
        self.positions = self._fetch_positions()


    def __iter__(self) -> Iterator[Position]:
        return iter(self.positions)


    def _fetch_positions(self) -> List[Position]:
        """Fetches the position data from the database and stores it in the portfolio instance"""

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