from sqlite3 import Connection

def _insert_portfolio(connection: Connection) -> None:
    
    # Insert portfolio into database
    connection.execute(
        """
        INSERT OR IGNORE INTO portfolios (
            portfolio_id,
            portfolio_name,
            base_currency
        )
        VALUES (?, ?, ?)
        """,
        (
            "DEMO",
            "Demo Portfolio",
            "USD"
        )
    )

    connection.commit()


def _insert_positions(connection: Connection) -> None:

    # Define positions
    positions = [
        ("DEMO", "AAPL", 100.0, 210.0),
        ("DEMO", "MSFT", 50.0, 450.0),
    ]

    # Insert positions into portfolio
    connection.executemany(
        """
        INSERT INTO positions (
            portfolio_id,
            instrument_id,
            quantity,
            market_price
        )
        VALUES (?, ?, ?, ?)
        ON CONFLICT (portfolio_id, instrument_id)
        DO UPDATE SET
            quantity = excluded.quantity,
            market_price = excluded.market_price
        """,
        positions
    )
    
    connection.commit()