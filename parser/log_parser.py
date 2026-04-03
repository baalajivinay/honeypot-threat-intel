import json
import sqlite3
import os

LOG_PATH = os.path.expanduser("~/honeypot-threat-intel/cowrie/var/log/cowrie/cowrie.json")
DB_PATH = os.path.expanduser("~/honeypot-threat-intel/data/attacks.db")

def parse_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(LOG_PATH, "r") as f:
        for line in f:
            try:
                event = json.loads(line.strip())

                eventid = event.get("eventid", "")

                if eventid in ["cowrie.login.success", "cowrie.login.failed"]:
                    cursor.execute('''
                        INSERT INTO attacks (timestamp, src_ip, username, password, session, event_type, sensor)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        event.get("timestamp"),
                        event.get("src_ip"),
                        event.get("username"),
                        event.get("password"),
                        event.get("session"),
                        eventid,
                        event.get("sensor")
                    ))

            except json.JSONDecodeError:
                continue

    conn.commit()
    conn.close()
    print("Logs parsed and saved to database.")

if __name__ == "__main__":
    parse_logs()
