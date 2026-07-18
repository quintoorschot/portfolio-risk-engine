from src.db.repositories import *
from src.db.tools import show_positions, initialize_database, get_prices_for_ticker
from src.market_data import store_historical_prices, get_stored_historical_prices
from src.dataclasses.Returns import Returns
from src.dataclasses.Portfolio import Portfolio
from typing import List
import pandas as pd

TICKERS: List[str] = ["AAPL", "MSFT"]

def main() -> None:
    
    connection: Connection = initialize_database()

    store_historical_prices(connection, TICKERS)

    portfolio: Portfolio = Portfolio(connection, "DEMO")
    print(portfolio.positions)

    print("Historical VaR:", portfolio.historical_var(confidence_interval=0.95))

    connection.close()


if __name__ == "__main__":
    main()