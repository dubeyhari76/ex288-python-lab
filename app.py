import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    # Get the greeting from the Environment, default to "Hello" if missing
    greeting = os.environ.get('GREETING', 'Hello')
    pod_name = os.environ.get('HOSTNAME', 'Localhost')
    
    return f"{greeting}! Served from Pod: {pod_name}\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)