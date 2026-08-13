import os
import sqlite3

DATABASE_NAME = "finance.db"
# Use a path relative to this file so the DB is created next to the project
DB_PATH = os.path.join(os.path.dirname(__file__), DATABASE_NAME)


def connect_db():
    """Return a sqlite3.Connection with a convenient row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    """Create the transactions table if it doesn't exist."""
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                transaction_date TEXT NOT NULL
            )
        """)