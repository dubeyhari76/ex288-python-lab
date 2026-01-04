# OpenShift Architect Lab (EX288) - Visitor Log App

## Project Overview
This repository contains a Python Flask microservice designed for the **Red Hat Certified Specialist in OpenShift Application Development (EX288)** practice. It demonstrates advanced OpenShift concepts including Source-to-Image (S2I) customization, ConfigMaps, Persistent Volume Claims (PVC), Liveness/Readiness Probes, and Sidecar patterns.

## Repository Structure

*   **`visitor_log.py`**: The main application logic (Flask) that replaces the standard `app.py`.
*   **`CHEATSHEET.md`**: A consolidated exam review covering all 4 days of pillars/phases.
*   **`TRACKER.md`**: A comprehensive daily log of the "Architect's Journey", documenting commands, troubleshooting steps, and lessons learned.
*   **`VISITOR_LOG_GUIDE.md`**: Detailed documentation for the application endpoints and architecture.
*   **`.s2i/environment`**: specific configuration to tell the Python builder to run `visitor_log.py` instead of `app.py`.
*   **`openshift-python-lab/`**: Contains the original/legacy reference code.

## Getting Started (Binary Build)

Since this project simulates a local development environment without a remote Git connection for the build, we use **Binary Builds**.

1.  **Create the Application**:
    ```bash
    oc new-app python:3.9-ubi8~. --name=visitor-app
    ```
2.  **Start the Build**:
    ```bash
    oc start-build visitor-app --from-dir=. --follow
    ```
3.  **Expose the Service**:
    ```bash
    oc expose svc/visitor-app
    ```

## Architect's Journey (Retrospective)

A summary of the key phases covered in `TRACKER.md`.

### Day 1: Foundation (Phases 0.1 - 0.4)
*   Basic Build & Deployment using Binary S2I.
*   ConfigMap injection for environment variables.
*   Debugging pods with `oc exec`.

### Day 2: Persistence & Health (Phases 1 - 5)
*   **Persistence**: decoupled storage using PVCs mounted at `/mnt/data`.
*   **Health**: Implemented Liveness (restart dead pods) and Readiness (traffic flow) probes.
*   **Resource Management**: Set requests and limits for QoS.

### Day 3: Advanced Architecture (Phases 8 - 10)
*   **Init Containers**: Used `busybox` to prepopulate data before the app starts.
*   **Service Accounts**: Granted `view` permissions to the pod to talk to the OpenShift API.
*   **Sidecars**: Added a logging sidecar to tail logs in real-time.

### Day 4: Automation & Guardrails (Phases 11 - 14)
*   **Build Hooks**: Added post-commit hooks to run syntax checks before pushing images.
*   **Triggers**: Configured automatic rollouts on image changes.
*   **Promotion**: Tagging images from `:latest` to `:prod` for stable releases.