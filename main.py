from src.db.repositories import *
from src.db.connection import database_connection
from src.market_data import load_price_data
from src.dataclasses.Portfolio import Portfolio
from typing import List
# from src.var import calculate_historical_var, calculate_parametric_var
from src.backtesting import backtest_historical_var
from src.dataclasses.VaRBacktestResult import VaRBacktestSummary

from src.new_var import calculate_historical_var
from src.market_data import get_price_data
import pandas as pd

TICKERS: List[str] = ["AAPL", "MSFT"]    

def main() -> None:
    
    with database_connection() as connection:

        load_price_data(connection, TICKERS)

        portfolio: Portfolio = Portfolio(connection, "DEMO")

        daily_pnl: pd.Series = portfolio._get_historical_pnl(connection)

        print("Historical VaR (95%, 1 day):", calculate_historical_var(daily_pnl, confidence_level=0.95, horizon_days=1))
        # print("Parametric VaR (95%, 1 day):", calculate_parametric_var(connection, portfolio, confidence_level=0.95, horizon_days=1))

        # backtest_summary: VaRBacktestSummary = backtest_historical_var(connection, portfolio)
        # print(backtest_summary)


if __name__ == "__main__":
    main()