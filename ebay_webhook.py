from flask import Flask, request, jsonify
from config import VERIFICATION_TOKEN  # Import token

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "✅ eBay Webhook Server is Running!", 200

@app.route("/ebay-notifications", methods=["POST"])
def ebay_notifications():
    """
    Handles incoming notifications from eBay, including challenge-response verification.
    """
    data = request.json
    print(f"🔹 Received eBay Notification: {data}")  # Logs request

    # eBay requires a challenge-response verification
    if "challengeResponse" in data:
        return jsonify({
            "challengeResponse": data["challengeResponse"],
            "verificationToken": VERIFICATION_TOKEN
        })

    return jsonify({"status": "Received"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)