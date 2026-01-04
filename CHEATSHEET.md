# EX288 Architect’s Cheat Sheet 📜

This covers every pillar we have mastered over the last four days, organized by functional domain to help you navigate the exam environment quickly.

## 🛠️ Project & Basic Resource Management
Commands for setting up your environment and investigating issues.

| Command | Usage |
| :--- | :--- |
| `oc new-project <name>` | Create and switch to a new project. |
| `oc project <name>` | Switch to an existing project. |
| `oc get all` | List all resources in the current namespace. |
| `oc describe <type>/<name>` | Detailed view of a resource (check for errors/events). |
| `oc logs <pod_name> -f` | Follow live application logs. |
| `oc delete all -l app=<label>` | Clean up all resources associated with a specific app. |
| `oc explain <resource>.<path>` | Built-in documentation (e.g., `oc explain deploy.spec.template`). |

## 🏗️ Builds & ImageStreams (Pillars 1, 10, 12)
Managing how code becomes images and how those images are versioned.

```bash
# Binary Builds: Upload local code to the cluster
oc new-app python:3.9-ubi8~. --name=myapp
oc start-build myapp --from-dir=. --follow

# Post-Commit Hooks: Adding build-time quality gates
oc set build-hook bc/myapp --post-commit --command -- python3 -m py_compile app.py

# Image Tagging & Promotion
oc get is                                             # View ImageStreams and tags
oc tag myapp:latest myapp:prod                        # Promote 'latest' to 'prod'
oc tag myapp:latest myapp:v1.0                        # Versioning an image
```

## ⚙️ Configuration & Secrets (Pillar 2)
Decoupling application logic from data.

```bash
# ConfigMaps: Non-sensitive data
oc create cm my-config --from-literal=KEY=VALUE
oc set env deployment/myapp --from=configmap/my-config

# Secrets: Sensitive data (passwords, keys)
oc create secret generic my-secret --from-literal=PASSWORD=redhat
oc set env deployment/myapp --from=secret/my-secret

# Mounting as Volumes (Alternative to Env Vars)
oc set volume deployment/myapp --add --name=cfg-vol --type=configmap --configmap-name=my-config --mount-path=/etc/config
```

## 🩺 Health Probes & Resource Management (Pillars 3, 4, 7)
Ensuring stability, self-healing, and fair resource allocation.

```bash
# Probes: Liveness (Restart) and Readiness (Traffic)
oc set probe deployment/myapp --liveness --get-url=http://:8080/health --initial-delay-seconds=15
oc set probe deployment/myapp --readiness --get-url=http://:8080/ --initial-delay-seconds=5

# Resource Requests & Limits
# Request = Reservation; Limit = Hard Ceiling
oc set resources deployment/myapp --requests=cpu=10m,memory=64Mi --limits=cpu=200m,memory=512Mi

# Monitoring Usage
oc adm top pods                                       # View real-time CPU/Memory usage
```

## 💾 Storage & Persistence (Pillar 5)
Managing the lifecycle of data.

```bash
# Add a Persistent Volume Claim (PVC) and mount it in one step
oc set volume deployment/myapp --add \
    --name=data-vol \
    --type=pvc \
    --claim-name=data-pvc \
    --claim-size=1Gi \
    --mount-path=/mnt/data

# Verify Storage
oc exec <pod_name> -- df -h /mnt/data                 # Check mount and capacity
```

## 🧬 Multi-Container Pods (Pillars 8, 9)
Configuring Init containers, Sidecars, and Security Identities.

```bash
# Service Accounts & RBAC
oc create sa monitor-admin                            # Create identity
oc policy add-role-to-user view -z monitor-admin      # Grant 'view' permission to SA
oc set serviceaccount deployment/myapp monitor-admin  # Attach SA to Pod

# Multi-Container Logging/Execution
oc logs <pod_name> -c sidecar-logger                  # View specific container logs
oc exec <pod_name> -c visitor-app -- ls /tmp          # Run command in specific container

# Manual Configuration (Init Containers / Sidecars)
oc edit deployment/myapp                              # Manually add container specs
```

## 🤖 Automation & Networking (Pillars 11, 13)
Triggers and external access.

```bash
# Triggers: Automatic rollouts
oc set triggers deployment/myapp --from-image=myapp:prod -c myapp --auto
oc set triggers deployment/myapp --manual             # Disable auto-triggers

# Networking: Services and Routes
oc expose deployment/myapp --port=8080                # Create Service
oc create route edge --service=myapp                  # Create Secure (Edge) Route
oc get route                                          # Find external URL
```
