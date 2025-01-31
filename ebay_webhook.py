import hashlib
import sqlite3
from flask import Flask, request, jsonify
from config import VERIFICATION_TOKEN  # Import your verification token

app = Flask(__name__)

WEBHOOK_URL = "https://ebay-webhook.onrender.com/ebay-notifications"  # Replace with your actual URL

# Ensure the database and table exist
conn = sqlite3.connect("ebay_notifications.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        event_data TEXT,
        received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()
conn.close()

@app.route("/", methods=["GET"])
def home():
    return "✅ eBay Webhook Server is Running!", 200

@app.route("/ebay-notifications", methods=["GET", "POST"])
def ebay_notifications():
    """
    Handles eBay webhook validation and incoming notifications.
    """
    if request.method == "GET":
        challenge_code = request.args.get("challenge_code")

        if challenge_code:
            combined_string = challenge_code + VERIFICATION_TOKEN + WEBHOOK_URL
            hashed_response = hashlib.sha256(combined_string.encode('utf-8')).hexdigest()

            response_data = {"challengeResponse": hashed_response}
            print(f"🔹 Responding to eBay verification: {response_data}")

            return jsonify(response_data), 200

    elif request.method == "POST":
        # Store incoming eBay notifications in SQLite database
        data = request.json
        event_type = data.get("metadata", {}).get("topic", "Unknown")
        event_data = str(data)

        conn = sqlite3.connect("ebay_notifications.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notifications (event_type, event_data) VALUES (?, ?)", (event_type, event_data))
        conn.commit()
        conn.close()

        print(f"✅ Stored eBay Notification in DB: {data}")
        return jsonify({"status": "Received"}), 200

    return jsonify({"error": "Invalid request method"}), 405

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

