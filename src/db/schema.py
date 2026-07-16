from sqlite3 import Connection

def create_tables(connection: Connection) -> None:
    
    # Create portfolios table
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS portfolios (
            portfolio_id TEXT PRIMARY KEY,
            portfolio_name TEXT NOT NULL,
            base_currency TEXT NOT NULL
        )
        """
    )

    # Create positions table
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS positions (
            position_id INTEGER PRIMARY KEY AUTOINCREMENT,
            portfolio_id TEXT NOT NULL,
            instrument_id TEXT NOT NULL,
            quantity REAL NOT NULL,
            market_price REAL NOT NULL,

            UNIQUE (portfolio_id, instrument_ID)

            FOREIGN KEY (portfolio_id)
                REFERENCES portfolios(portfolio_id)
        )
        """
    )

    # Create historical prices table
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS historical_prices (
            instrument_id TEXT NOT NULL,
            price_date TEXT NOT NULL,
            close_price REAL NOT NULL,
            PRIMARY KEY (instrument_id, price_date)
        )
        """
    )

    connection.commit()