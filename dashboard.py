import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

def get_notifications():
    conn = sqlite3.connect("ebay_notifications.db")
    cursor = conn.cursor()
    cursor.execute("SELECT event_type, event_data, received_at FROM notifications ORDER BY received_at DESC")
    notifications = cursor.fetchall()
    conn.close()
    return notifications

@app.route("/")
def home():
    notifications = get_notifications()
    return render_template("dashboard.html", notifications=notifications)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)  # Runs on port 5001
