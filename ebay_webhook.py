from flask import Flask, request, jsonify
from config import VERIFICATION_TOKEN  # Import your verification token

app = Flask(__name__)

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
            response = {
                "challengeResponse": challenge_code,
                "verificationToken": VERIFICATION_TOKEN
            }
            print(f"🔹 Responding to eBay verification: {response}")
            return jsonify(response), 200  # Ensure JSON response format

    elif request.method == "POST":
        # Handle incoming notifications from eBay
        data = request.json
        print(f"🔹 Received eBay Notification: {data}")
        return jsonify({"status": "Received"}), 200

    return jsonify({"error": "Invalid request method"}), 405

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)