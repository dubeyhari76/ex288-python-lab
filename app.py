import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    # In Kubernetes, the HOSTNAME is the Pod Name
    pod_name = os.environ.get('HOSTNAME', 'Localhost')
    return f"Hello! Served from Pod: {pod_name}\n"

if __name__ == "__main__":
    # OpenShift default python builder expects port 8080
    app.run(host='0.0.0.0', port=8080)