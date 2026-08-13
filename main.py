from src.db.repositories import *
from src.db.connection import database_connection
from src.market_data import load_price_data
from src.dataclasses.Portfolio import Portfolio
from src.dataclasses.VaRBacktestResult import VaRBacktestObservation, VaRBacktestSummary
from src.backtesting import backtest_historical_var, backtest_parametric_var
from typing import List

TICKERS: List[str] = ["AAPL", "MSFT"]    

def main() -> None:
    
    with database_connection() as connection:

        load_price_data(connection, TICKERS)

        portfolio: Portfolio = Portfolio(connection, "DEMO")
        print(portfolio)

        # print("Historical VaR (95%, 1 day):", portfolio.historical_var())
        # print("Historical CVaR (95%, 1 day):", portfolio.historical_cvar())


        # print("Parametric CVaR (95%, 1 day):", portfolio.parametric_cvar())

        # backtest_summary: VaRBacktestSummary = backtest_parametric_var(connection, portfolio)
        # print(backtest_summary)
        #print(backtest_summary.kupiec_test())


if __name__ == "__main__":
    main()