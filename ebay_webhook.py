import hashlib
from flask import Flask, request, jsonify
from config import VERIFICATION_TOKEN  # Import your verification token

app = Flask(__name__)

WEBHOOK_URL = "https://ebay-webhook.onrender.com/ebay-notifications"  # Replace with your actual URL

@app.route("/", methods=["GET"])
def home():
    return "✅ eBay Webhook Server is Running!", 200

@app.route("/ebay-notifications", methods=["GET", "POST"])
def ebay_notifications():
    """
    Handles eBay webhook validation and incoming notifications.
    """
    if request.method == "GET":
        # eBay sends a GET request with a challenge_code to verify the webhook
        challenge_code = request.args.get("challenge_code")

        if challenge_code:
            # Hash the challenge_code + verification_token + endpoint URL
            combined_string = challenge_code + VERIFICATION_TOKEN + WEBHOOK_URL
            hashed_response = hashlib.sha256(combined_string.encode('utf-8')).hexdigest()

            response_data = {"challengeResponse": hashed_response}

            print(f"🔹 Responding to eBay verification: {response_data}")  # Logs response to Render logs

            return jsonify(response_data), 200  # Ensure JSON response format

    elif request.method == "POST":
        # Handle incoming notifications from eBay
        data = request.json
        print(f"🔹 Received eBay Notification: {data}")
        return jsonify({"status": "Received"}), 200

    return jsonify({"error": "Invalid request method"}), 405

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
