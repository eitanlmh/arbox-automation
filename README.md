# arbox-automation

# 🧠 Arbox Automation Platform
A secure, containerized automation system for interacting with the Arbox platform via a Flask-based API. Designed to perform actions such as login, lesson booking, and synchronization — all while securely handling credentials through Vault.

# 🚀 Features
🔐 Secure secret management via HashiCorp Vault

🌐 Flask API for controlling automation steps (login, book lesson, etc.)

🧵 Background worker for periodic or triggered actions

🐳 Fully containerized using Docker & Docker Compose

🧠 Modular and scalable structure for future extensions

# 🗂️ Project Structure

```
arbox-automation/
├── app/
│   ├── __init__.py           # Initializes Flask app
│   ├── routes.py             # API endpoints
│   ├── arbox_client.py       # Logic to interact with Arbox
│   ├── worker.py             # Background worker process
│   └── vault.py              # Vault integration logic
│
├── secrets/
│   ├── policy.hcl            # Vault policy definition
│   └── .vault-token          # Vault root/dev token (dev only)
│
├── requirements.txt          # Python dependencies
├── Dockerfile                # Image definition
├── docker-compose.yml        # Compose multi-service setup
├── .env                      # Non-secret config
└── README.md                 # You are here
```
# 🛠️ Setup Instructions
1. Prerequisites
Docker & Docker Compose installed

Vault CLI (for managing secrets manually if needed)

2. Clone the Repository
```bash

git clone https://github.com/your-user/arbox-automation.git
cd arbox-automation
```
3. Define Secrets in Vault
Spin up Vault (via Docker Compose), then run:

```bash
docker exec -it arbox-automation-vault-1 sh
vault login root
```
Add Arbox credentials securely
```
vault kv put secret/arbox email="you@example.com" password="your_password"
```
You can modify secrets/policy.hcl and apply policies as needed.

# 4. Build and Run the Project
```
docker-compose up --build
```
This starts:

Flask API at http://localhost:5000

Vault at http://localhost:8200 (dev mode)

A worker who periodically performs sync tasks

# 🔌 API Endpoints
Method	Route	Description
POST	/login	Logs in to Arbox
POST	/book	Books a lesson by ID

Example request (book a lesson):

POST http://localhost:5000/book

```json
{
  "lesson_id": "123456"
}
```
# 🔐 Vault Integration
Uses hvac Python client to access Vault secrets at runtime.

All sensitive tokens and passwords are never hardcoded.

Vault token injected via Docker secret or env var.

# 🧪 Testing & Extending
Replace arbox_client.py logic with real Playwright/Selenium as needed.

Add more endpoints to routes.py to support new actions.

Implement task queue (e.g., Celery) for better background job management.

# 🧰 Technologies Used
Python 3.11

Flask

HashiCorp Vault

Docker + Docker Compose

(Optional) Selenium / Playwright / Requests

⚠️ Security Notes
Do not store real credentials in the .env or code.
