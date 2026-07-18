from src.db.repositories import *
from src.db.connection import database_connection
from src.market_data import load_price_data
from src.dataclasses.Portfolio import Portfolio
from typing import List

TICKERS: List[str] = ["AAPL", "MSFT"]

def main() -> None:
    
    with database_connection() as connection:

        load_price_data(connection, TICKERS)

        portfolio: Portfolio = Portfolio(connection, "DEMO")
        print(portfolio.positions)

        print("Historical VaR:", portfolio.historical_var(confidence_interval=0.95))
        print("Parametric VaR:", portfolio.parametric_var(confidence_interval=0.95))


if __name__ == "__main__":
    main()