from sqlite3 import Connection
import yfinance as yf
from typing import List
import pandas as pd

def download_price_data(tickers: str | List[str]) -> pd.DataFrame:
    """Downloads historical price data and returns it as DataFrame"""

    prices = yf.download(
        tickers=tickers,
        start="2024-01-01",
        end="2026-01-01",
        interval="1d",
        auto_adjust=True,
        progress=False,
    )

    if prices is None:
        raise RuntimeError(f"[ERROR] Failed to retrieve historical prices for {prices}")

    return prices


def load_price_data(connection: Connection, tickers: List[str] | str) -> None:
    """
    Download historical prices using `download_historical_prices`,
    reshape the data, and store it in the `historical_prices` table.
    """

    prices = download_price_data(tickers)

    prices = (
        prices["Close"].rename_axis("price_date")
        .reset_index()
        .melt(
            id_vars="price_date",
            var_name="instrument_id",
            value_name="market_price",
        )
    )

    prices.to_sql(
        "historical_prices",
        connection,
        if_exists="replace",
        index=False,
    )


def get_price_data(connection: Connection, ticker: str) -> pd.DataFrame:
    """Returns historical price data about the ticker passed into the function"""

    query = """
        SELECT price_date, instrument_id, market_price
        FROM historical_prices
        WHERE instrument_id = ?
        ORDER BY price_date
    """

    return pd.read_sql_query(query, connection, params=(ticker,), parse_dates=["price_date"])