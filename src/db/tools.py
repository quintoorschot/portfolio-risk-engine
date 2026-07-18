from src.db.connection import get_connection
from src.db.repositories import _insert_portfolio, _insert_positions
from src.db.schema import _create_tables
from sqlite3 import Connection, Cursor
import pandas as pd

def get_prices_for_ticker(connection: Connection, ticker: str) -> pd.DataFrame:
    query = """
        SELECT price_date, instrument_id, market_price
        FROM historical_prices
        WHERE instrument_id = ?
        ORDER BY price_date
    """

    return pd.read_sql_query(query, connection, params=(ticker,), parse_dates=["price_date"])


def show_positions(connection: Connection) -> None:
    cursor: Cursor = connection.execute(
        """
        SELECT
            instrument_id,
            quantity,
            market_price,
            quantity * market_price AS market_value
        FROM positions
        WHERE portfolio_id = ?
        ORDER BY instrument_id
        """,
        ("DEMO",),
    )

    rows = cursor.fetchall()

    for row in rows:
        instrument_id, quantity, market_price, market_value = row

        print(
            f"{instrument_id}: "
            f"{quantity:.0f} units × "
            f"${market_price:,.2f} = "
            f"${market_value:,.2f}"
        )

def initialize_database() -> Connection:

    connection: Connection = get_connection()

    _create_tables(connection)
    _insert_portfolio(connection)
    _insert_positions(connection)

    return connection