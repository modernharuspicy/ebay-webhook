from flask import Flask, request, jsonify

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
    print("🔹 Received eBay No
