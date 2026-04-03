import requests
import sqlite3
import os

DB_PATH = os.path.expanduser("~/honeypot-threat-intel/data/attacks.db")
WEBHOOK_URL = ""

def send_to_make():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM attacks ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        payload = {
            "id": row[0],
            "timestamp": row[1],
            "src_ip": row[2],
            "username": row[3],
            "password": row[4],
            "session": row[5],
            "event_type": row[6],
            "sensor": row[7]
        }

        response = requests.post(WEBHOOK_URL, json=payload)
        print(f"Sent to Make.com — Status: {response.status_code}")
    else:
        print("No attacks found in database.")

if __name__ == "__main__":
    send_to_make()
