from src.db.connection import get_connection
from src.db.schema import create_tables
from src.db.repositories import *
from src.db.tools import show_positions
import sqlite3

def main() -> None:
    
    connection: sqlite3.Connection = get_connection()

    try:
        create_tables(connection)
        insert_portfolio(connection)
        insert_positions(connection)
        show_positions(connection)
    finally:
        connection.close()


if __name__ == "__main__":
    main()