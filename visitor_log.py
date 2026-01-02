import os
import datetime
from flask import Flask

app = Flask(__name__)

@app.route('/')
def welcome():
    message = os.environ.get('WELCOME_MSG', 'Welcome to the Visitor Log App!')
    return message + "\n"

@app.route('/write')
def write_log():
    timestamp = datetime.datetime.now().isoformat()
    log_path = '/mnt/data/history.txt'
    
    try:
        # ensuring the directory exists is polite but strict requirement said "located at /mnt/data/history.txt"
        # I will assume the directory exists or just try to write.
        # If I can't write, it will error 500, which is fine for a demo app.
        with open(log_path, 'a') as f:
            f.write(f"{timestamp}\n")
        return f"Logged: {timestamp}\n", 200
    except Exception as e:
        return f"Failed to write log: {str(e)}\n", 500

@app.route('/health')
def health_check():
    return "OK\n", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
