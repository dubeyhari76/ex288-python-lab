# Visitor Log Application Documentation

## Overview
This document details the "Visitor Log" application, a Python Flask-based microservice designed for OpenShift deployment. It decouples the application entry point from the standard `app.py`, utilizes environment variables for configuration, and provides health endpoints for Kubernetes probes.

## Architecture

### 1. Application Logic (`visitor_log.py`)
The application is a single-file Flask server containing three critical routes:

*   **Welcome Route (`GET /`)**:
    *   **Function**: Reads the `WELCOME_MSG` environment variable.
    *   **Default**: "Welcome to the Visitor Log App!" if variable is missing.
    *   **Purpose**: Demonstrates configuration injection (ConfigMap).

*   **Write Route (`GET /write`)**:
    *   **Function**: Appends the current ISO timestamp to `/mnt/data/history.txt`.
    *   **Path**: `/mnt/data` is the target mount point for Persistent Volumes (PVC).
    *   **Purpose**: Validates storage persistence. *Note: Requires a writeable volume mounted at `/mnt/data`.*

*   **Health Route (`GET /health`)**:
    *   **Function**: Returns `OK` with status 200.
    *   **Purpose**: Used by OpenShift Readiness and Liveness probes.

### 2. Source-to-Image (S2I) Customization
To run `visitor_log.py` instead of the default `app.py` without changing the container run command manually, we utilize the S2I environment configuration.

*   **File**: `.s2i/environment`
*   **Content**: `APP_FILE=visitor_log.py`
*   **Effect**: The Red Hat Python builder image checks this file and updates the generated start script to execute `visitor_log.py` via Gunicorn.

## Deployment Strategy (Binary Build)

Since the code is developed locally without a remote Git repository, a **Binary Build** strategy is used.

### Commands Used

1.  **Create Application Placeholder**:
    ```bash
    oc new-app python:3.9-ubi9 --name=visitor-app --binary=true
    ```
    *   `--binary=true`: Tells OpenShift to wait for input from a local stream (archive) instead of cloning a Git repo.

2.  **Trigger Build**:
    ```bash
    oc start-build visitor-app --from-dir=.
    ```
    *   `--from-dir=.`: Uploads the current directory content to the builder.

3.  **Expose Service**:
    ```bash
    oc expose service/visitor-app
    ```

## Verification

To verify the application is running specifically `visitor_log.py`:

```bash
# Check the processes inside the pod
oc exec <pod_name> -- ps aux | grep visitor_log
```
You should see a Gunicorn process serving `visitor_log:app`.

## Troubleshooting

*   **"No such file or directory: /mnt/data/history.txt"**:
    The `/write` endpoint will fail with a 500 error if the `/mnt/data` directory does not exist. Ensure a Persistent Volume Claim (PVC) is mounted to the deployment at that path.

    ```bash
    oc set volume deployment/visitor-app --add --name=data-vol --mount-path=/mnt/data --type=pvc --claim-name=my-pvc
    ```
