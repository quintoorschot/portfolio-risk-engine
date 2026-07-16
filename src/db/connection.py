from pathlib import Path
import sqlite3

DATABASE_PATH = Path('data/database.db')

def get_connection(database_path: Path = DATABASE_PATH) -> sqlite3.Connection:
    """Create and configure SQLite database connection"""

    # Create the data directory if it doesn't exist yet
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Create connection to SQLite database
    connection: sqlite3.Connection = sqlite3.connect(database_path)

    return connection