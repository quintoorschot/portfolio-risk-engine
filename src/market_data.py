from sqlite3 import Connection
import yfinance as yf
from typing import List
import pandas as pd

def get_historical_prices(tickers: str | List[str]) -> pd.DataFrame:

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


def store_historical_prices(connection: Connection, tickers: List[str] | str) -> None:

    prices = get_historical_prices(tickers)

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


def get_stored_historical_prices(connection: Connection) -> pd.DataFrame:

    query: str = """
        SELECT
            price_date,
            instrument_id,
            market_price
        FROM historical_prices
        ORDER BY instrument_id, price_date
    """

    return pd.read_sql_query(query, connection, parse_dates=['price_date'])