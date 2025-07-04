# Webhook Repo

A Flask-based GitHub Webhook receiver that listens for `push` and `pull_request` events, stores them in MongoDB, and displays them in a simple polling UI.

## ✅ Features

- Accepts GitHub webhook events at `/webhook`
- Stores minimal event data in MongoDB:
  - `author`
  - `from_branch`
  - `to_branch`
  - `timestamp`
  - `action` (`push`, `pull_request`, or `merge`)
- `/events` returns latest 20 events
- Frontend UI polls `/events` every 15 seconds
- `/health` route for uptime checks

## 🧰 Tech Stack

- Python 3.8+
- Flask
- MongoDB (local or Atlas)
- HTML/CSS/JS (Frontend)
- Flask-CORS
- dotenv

## 📦 Project Structure

.
├── app.py
├── requirements.txt
├── .env (you create this)
├── static/
│ └── index.html
└── README.md


## 🧪 Local Setup

### 1. Clone and Install

git clone https://github.com/SwapnilShukla-1409/webhook-repo.git
cd webhook-repo

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
2. Create .env File
dotenv

MONGO_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/webhook_db
GITHUB_WEBHOOK_SECRET=your_secret_here
3. Run the App
python app.py
App runs on http://localhost:5000.

4. Optional: Tunnel for GitHub Webhooks
If testing locally, expose your server:

ngrok http 5000
Set the GitHub Webhook Payload URL to:


https://<ngrok-id>.ngrok.io/webhook


🌐 Web UI
Visit / (root URL) to view recent events.

Supported Event Formats:
✅ Alice pushed to main on 4 July 2025 – 10:45 PM UTC

✅ Bob submitted a pull request from feature/x to main on ...

✅ Charlie merged branch feature/y to main on ...

📡 Endpoints
Route	Method	Description
/webhook	POST	Receives GitHub events (push, PR)
/events	GET	Returns latest 20 events (JSON)
/health	GET	Health check for uptime monitors
/	GET	Web UI (static HTML/JS)

👥 Maintainer
Swapnil Shukla
MIT License © 2025