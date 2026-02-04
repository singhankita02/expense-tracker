import sqlite3
from decimal import Decimal
from datetime import datetime

def get_connection():
    return sqlite3.connect("expenses.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id TEXT PRIMARY KEY,
            client_request_id TEXT UNIQUE,
            amount TEXT,
            category TEXT,
            description TEXT,
            date TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()
