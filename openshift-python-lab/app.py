import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    greeting = os.environ.get('GREETING', 'Hello')
    pod_name = os.environ.get('HOSTNAME', 'Localhost')
    return f"{greeting}! Served from Pod: {pod_name}\n"

# --- ADD THIS SECTION ---
@app.route('/health')
def health_check():
    # In a real app, you'd check DB connections here
    return jsonify(status="UP"), 200
# ------------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)