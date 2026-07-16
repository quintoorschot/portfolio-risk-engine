from sqlite3 import Connection

def show_positions(connection: Connection) -> None:
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