from src.db.connection import get_connection
from src.db.schema import create_tables
from src.db.repositories import *
from src.db.tools import show_positions
from src.market_data import store_historical_prices, get_stored_historical_prices
from typing import List
import sqlite3

TICKERS: List[str] = ["AAPL", "MSFT"]

def main() -> None:
    
    connection: sqlite3.Connection = get_connection()

    try:
        create_tables(connection)
        insert_portfolio(connection)
        insert_positions(connection)
        show_positions(connection)

        store_historical_prices(connection, TICKERS)
        print(get_stored_historical_prices(connection))

    finally:
        connection.close()


if __name__ == "__main__":
    main()