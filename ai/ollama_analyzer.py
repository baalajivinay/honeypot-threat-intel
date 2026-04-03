import requests
import sqlite3
import os

DB_PATH = os.path.expanduser("~/honeypot-threat-intel/data/attacks.db")

def analyze_attack(attack):
    prompt = f"""You are a cybersecurity analyst. Analyze this attack and give a short threat summary in 3 lines max.

Attack details:
- IP: {attack['src_ip']}
- Username tried: {attack['username']}
- Password tried: {attack['password']}
- Event type: {attack['event_type']}
- Timestamp: {attack['timestamp']}

Give: threat level (LOW/MEDIUM/HIGH), attack type, and recommendation."""

    response = requests.post(
        url="http://localhost:11434/api/generate",
        json={
            "model": "dolphin-mistral:7b",
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )

    result = response.json()
    try:
        return result["response"]
    except Exception as e:
        return f"AI analysis failed: {result}"

def get_latest_attack():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attacks ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "timestamp": row[1],
            "src_ip": row[2],
            "username": row[3],
            "password": row[4],
            "session": row[5],
            "event_type": row[6],
            "sensor": row[7]
        }
    return None

if __name__ == "__main__":
    attack = get_latest_attack()
    if attack:
        print("Analyzing attack...")
        summary = analyze_attack(attack)
        print("\n🤖 AI Threat Summary:")
        print(summary)
    else:
        print("No attacks found.")
