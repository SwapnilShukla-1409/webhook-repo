from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv("MONGO_URI"))
db = client["webhook_db"]
collection = db["events"]

# Health‑check endpoint
@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

# Webhook receiver (accepts both /webhook and /webhook/)
@app.route("/webhook", methods=["POST"], strict_slashes=False)
def webhook():
    # Parse JSON body
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"msg": "Invalid JSON"}), 400

    event_type = request.headers.get("X-GitHub-Event")
    if not event_type:
        return jsonify({"msg": "Missing event type"}), 400

    # Handle GitHub’s ping
    if event_type == "ping":
        # GitHub sends ping when you first register or update a webhook
        return jsonify({"msg": "pong"}), 200

    # Handle pushes
    if event_type == "push":
        doc = {
            "action": "push",
            "author": data.get("pusher", {}).get("name"),
            "from_branch": None,
            "to_branch": data.get("ref", "").split("/")[-1],
            "timestamp": datetime.utcnow()
        }

    # Handle pull requests (opened/synced/closed)
    elif event_type == "pull_request":
        pr = data.get("pull_request", {})
        # Distinguish merge vs open/update
        if pr.get("merged"):
            action = "merge"
        else:
            action = pr.get("action", "pull_request")
        doc = {
            "action": action,
            "author": pr.get("user", {}).get("login"),
            "from_branch": pr.get("head", {}).get("ref"),
            "to_branch": pr.get("base", {}).get("ref"),
            "timestamp": datetime.utcnow()
        }

    else:
        # All other events: ignore
        return jsonify({"msg": f"Unhandled event type: {event_type}"}), 400

    # Store to MongoDB
    collection.insert_one(doc)
    return jsonify({"msg": f"{event_type} event received"}), 200



@app.route("/events", methods=["GET"])
def get_events():
    events = list(collection.find().sort("timestamp", -1).limit(20))
    for e in events:
        e["_id"] = str(e["_id"])
        e["timestamp"] = e["timestamp"].strftime("%d %B %Y - %I:%M %p UTC")
    return jsonify(events)


if __name__ == "__main__":
    # Bind to 0.0.0.0 so tunnels like ngrok/localtunnel can reach it
    app.run(host="0.0.0.0", port=5000, debug=True)
