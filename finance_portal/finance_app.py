import os
import datetime
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configuration
WELCOME_MSG = os.getenv('WELCOME_MSG', 'Welcome to Finance Portal')
LOG_FILE_PATH = '/mnt/finance/logs/app.log'
STATUS_FILE_PATH = '/mnt/finance/status.txt'
K8S_TOKEN_PATH = '/var/run/secrets/kubernetes.io/serviceaccount/token'
K8S_API_URL = 'https://kubernetes.default.svc/api/v1/namespaces/dubeyhari76-dev/pods'

@app.route('/')
def home():
    return WELCOME_MSG

@app.route('/write')
def write_log():
    try:
        timestamp = datetime.datetime.now().isoformat()
        with open(LOG_FILE_PATH, 'a') as f:
            f.write(f"{timestamp}\n")
        return f"Appended {timestamp} to log."
    except Exception as e:
        return f"Error writing to log: {str(e)}", 500

@app.route('/read')
def read_log():
    try:
        if os.path.exists(LOG_FILE_PATH):
            with open(LOG_FILE_PATH, 'r') as f:
                content = f.read()
            return content, 200, {'Content-Type': 'text/plain'}
        return "Log file empty or does not exist."
    except Exception as e:
        return f"Error reading log: {str(e)}", 500

@app.route('/health')
def health():
    return jsonify({"status": "UP"}), 200

@app.route('/whoami')
def whoami():
    try:
        if not os.path.exists(K8S_TOKEN_PATH):
            return "Service Account token not found. Not running in K8s or paths differ.", 404
        
        with open(K8S_TOKEN_PATH, 'r') as f:
            token = f.read().strip()
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        
        # Verify=False because internal K8s API CA might not be in system store by default in all envs,
        # but typically in a pod we should use /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        # For this exercise, simple requests call.
        response = requests.get(K8S_API_URL, headers=headers, verify=False, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            return f"Pod count in namespace 'dubeyhari76-dev': {len(items)}"
        else:
            return f"K8s API Error: {response.status_code} - {response.text}", 502

    except Exception as e:
        return f"Error in /whoami: {str(e)}", 500

def startup_tasks():
    # Log APP_MODE
    app_mode = os.getenv('APP_MODE', 'NOT_SET')
    print(f"APP_MODE: {app_mode}")
    
    # Check DB_PASSWORD (mock secure check)
    if os.getenv('DB_PASSWORD'):
        print("DB Connection Secure")
        
    # Read status.txt
    if os.path.exists(STATUS_FILE_PATH):
        try:
            with open(STATUS_FILE_PATH, 'r') as f:
                print(f"Status Data: {f.read().strip()}")
        except Exception as e:
            print(f"Error reading status file: {e}")
    else:
        print(f"Status file not found at {STATUS_FILE_PATH}")

# Run startup tasks locally if executed directly, 
# but effectively we want this to run when app starts.
# In a real WSGI app (gunicorn), this might need to be hooked differently, 
# but for this script top-level execution works if run as main, 
# or we can just print it at module level.
startup_tasks()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
