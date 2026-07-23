from src.db.repositories import *
from src.db.connection import database_connection
from src.market_data import load_price_data
from src.dataclasses.Portfolio import Portfolio
from typing import List
from src.var import calculate_historical_var

TICKERS: List[str] = ["AAPL", "MSFT"]

def main() -> None:
    
    with database_connection() as connection:

        load_price_data(connection, TICKERS)

        portfolio: Portfolio = Portfolio(connection, "DEMO")
        # print(portfolio.positions, "\n")

        print("Historical VaR:", calculate_historical_var(connection, portfolio, 0.95))
        # print("Parametric VaR:", portfolio.parametric_var(confidence_interval=0.95))


if __name__ == "__main__":
    main()