from src.db.repositories import *
from src.db.tools import show_positions, initialize_database, get_prices_for_ticker
from src.market_data import store_historical_prices, get_stored_historical_prices
from src.var import calculate_historic_var
from src.dataclasses.Returns import Returns
from typing import List
import pandas as pd

TICKERS: List[str] = ["AAPL", "MSFT"]

def main() -> None:
    
    connection: Connection = initialize_database()

    store_historical_prices(connection, TICKERS)

    # show_positions(connection)
    # print(get_stored_historical_prices(connection))

    prices: pd.DataFrame = get_prices_for_ticker(connection, "AAPL")
    returns = Returns(prices)

    print(calculate_historic_var(10_000, returns))

    connection.close()


if __name__ == "__main__":
    main()