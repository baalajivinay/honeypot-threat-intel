from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.expanduser("~/honeypot-threat-intel/data/attacks.db")

def get_attacks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attacks ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/attacks')
def attacks():
    rows = get_attacks()
    data = []
    for row in rows:
        data.append({
            "id": row[0],
            "timestamp": row[1],
            "src_ip": row[2],
            "username": row[3],
            "password": row[4],
            "session": row[5],
            "event_type": row[6],
            "sensor": row[7]
        })
    return jsonify(data)

@app.route('/api/stats')
def stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM attacks")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(DISTINCT src_ip) FROM attacks")
    unique_ips = cursor.fetchone()[0]
    cursor.execute("SELECT src_ip, COUNT(*) as count FROM attacks GROUP BY src_ip ORDER BY count DESC LIMIT 5")
    top_ips = cursor.fetchall()
    cursor.execute("SELECT username, COUNT(*) as count FROM attacks GROUP BY username ORDER BY count DESC LIMIT 5")
    top_usernames = cursor.fetchall()
    conn.close()
    return jsonify({
        "total": total,
        "unique_ips": unique_ips,
        "top_ips": top_ips,
        "top_usernames": top_usernames
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
