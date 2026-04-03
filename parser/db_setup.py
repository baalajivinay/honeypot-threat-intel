import sqlite3
import os

DB_PATH = os.path.expanduser("~/honeypot-threat-intel/data/attacks.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            src_ip TEXT,
            username TEXT,
            password TEXT,
            session TEXT,
            event_type TEXT,
            sensor TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
