from pathlib import Path
import sqlite3

DATABASE_PATH = Path('data/database.db')

def main() -> None:
    
    # Create the data directory if it doesn't exist yet
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Open the database (creates one if it doesn't exist yet)
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        create_tables(connection)
    finally:
        connection.close()


def create_tables(connection: sqlite3.Connection) -> None:
    
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

            FOREIGN KEY (portfolio_id)
                REFERENCES portfolios(portfolio_id)
        )
        """
    )

    connection.commit()


def insert_portfolio(connection: sqlite3.Connection) -> None:
    
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


def insert_positions(connection: sqlite3.Connection) -> None:

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
            market_price,
        )
        VALUES (?, ?, ?, ?)
        """,
        positions
    )
    
    connection.commit()


def show_positions(connection: sqlite3.Connection) -> None:
    cursor = connection.execute(
        """
        SELECT
            instrument_id,
            quantity,
            market_price,
            quantity * market_price AS market_value
        FROM positions
        WHERE portfolio_id = ?
        ORDER BY instrument_id
        """,
        ("DEMO",),
    )

    rows = cursor.fetchall()

    for row in rows:
        instrument_id, quantity, market_price, market_value = row

        print(
            f"{instrument_id}: "
            f"{quantity:.0f} units × "
            f"${market_price:,.2f} = "
            f"${market_value:,.2f}"
        )


if __name__ == "__main__":
    main()