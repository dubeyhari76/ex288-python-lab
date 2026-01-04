import os
import time
from flask import Flask, jsonify

app = Flask(__name__)

# Pillar 2: Config/Secrets
WELCOME_MSG = os.environ.get('WELCOME_MSG', 'Welcome to the Legacy App!')
LOG_FILE = "/mnt/data/history.txt"

@app.route('/')
def home():
    return f"{WELCOME_MSG}\n"

@app.route('/write')
def write_log():
    # Pillar 4: Persistence
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(f"Visitor at: {time.ctime()}\n")
        return "Log Entry Written!\n"
    except Exception as e:
        return f"Error writing log: {str(e)}\n", 500

@app.route('/health')
def health():
    # Pillar 3: Probes
    return jsonify(status="UP"), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)