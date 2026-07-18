from src.db.repositories import _insert_portfolio, _insert_positions
from src.db.schema import _create_tables
from contextlib import contextmanager
from collections.abc import Iterator
from pathlib import Path
import sqlite3

DATABASE_PATH = Path('data/database.db')

@contextmanager
def database_connection() -> Iterator[sqlite3.Connection]:
    connection: sqlite3.Connection = _get_connection()

    try:
        _create_tables(connection)
        _insert_portfolio(connection)
        _insert_positions(connection)
        connection.commit()

        yield connection
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def _get_connection(database_path: Path = DATABASE_PATH) -> sqlite3.Connection:
    """Create and configure SQLite database connection"""

    # Create the data directory if it doesn't exist yet
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Create connection to SQLite database
    connection: sqlite3.Connection = sqlite3.connect(database_path)

    return connection