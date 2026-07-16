from src.db.repositories import *
from src.db.tools import show_positions, initialize_database, get_prices_for_ticker
from src.market_data import store_historical_prices, get_stored_historical_prices
from src.dataclasses.Returns import Returns
from typing import List

TICKERS: List[str] = ["AAPL", "MSFT"]


import pandas as pd
import numpy as np

def calculate_historic_var(values: Returns, confidence_interval: float = 0.95) -> float:

    return -1


def main() -> None:
    
    connection: Connection = initialize_database()

    store_historical_prices(connection, TICKERS)

    # show_positions(connection)
    # print(get_stored_historical_prices(connection))

    print(get_prices_for_ticker(connection, "AAPL"))

    connection.close()


if __name__ == "__main__":
    main()