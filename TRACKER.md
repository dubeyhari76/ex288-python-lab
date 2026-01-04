# OpenShift Architect Tracker: Exercise EX288 🚀

## Day 1: Build, Deployment & ConfigMaps
**Date:** 01/01/2026

### 🏗️ Phase 0.1: Build & Deployment
* **Binary Build:** `oc start-build myapp --from-dir=. --follow`
* **Route Verification:** `oc describe route myapp`
* **Service Verification:** `oc describe svc myapp`

### ⚙️ Phase 0.2: Configuration (ConfigMaps)
* **Create ConfigMap:** `oc create configmap app-config --from-literal=GREETING=Namaste`
* **Link to Deployment:** `oc set env deployment/myapp --from=configmap/app-config`
* **View ConfigMap Details:** `oc get cm app-config -o yaml`
* **Replace ConfigMap Content:**
  ```bash
  oc create configmap app-config --from-literal=GREETING="Radhey Radhey Ji" --dry-run=client -o yaml | oc replace -f -
  ```

### 🔍 Phase 0.3: Debugging & Maintenance
* **Inspect Pod Environment:** `oc describe pod <pod_name>`
* **Verify Filesystem Code:** `oc exec <pod_name> -- cat app.py`
* **Check Internal Environment:** `oc exec <pod_name> -- env | grep GREETING`
* **Test Local App Response:** `oc exec <pod_name> -- curl -s localhost:8080`
* **Remove Specific Env Var:** `oc set env deployment/myapp GREETINGS-`

### 📈 Phase 0.4: Lifecycle & Scaling
* **Trigger Rolling Restart:** `oc rollout restart deployment/myapp`
* **Scale Replicas:** `oc scale deployment myapp --replicas=3`
* **Test Load Balancing:** `for i in {1..5}; do curl -s <route_url>; done`

## Day 2: Python Health & Persistence App
**Date:** 01/02/2026
**Status:** Foundation Complete | Ready for "Legacy Migrator" Challenge

### 🏗️ Phase 1: Build & Deploy (Binary S2I)
Moving local code to the cluster without a Git repository.

| Step | Task | Command |
| :--- | :--- | :--- |
| 1 | Create App | `oc new-app python:3.9-ubi8~. --name=myapp` |
| 2 | Start Build | `oc start-build myapp --from-dir=. --follow` |
| 3 | Expose App | `oc expose svc/myapp` |

### ⚙️ Phase 2: Configuration & Security
Decoupling application logic from configuration and secrets.

**ConfigMaps (Public Settings)**
```bash
# Create from literal
oc create cm app-config --from-literal=GREETING="Radhey Radhey Ji"

# Inject into deployment
oc set env deployment/myapp --from=configmap/app-config
```

**Secrets (Sensitive Data)**
```bash
# Create Secret
oc create secret generic app-secrets --from-literal=API_KEY=RedHat-2026-Secret

# Inject into deployment
oc set env deployment/myapp --from=secret/app-secrets
```

### 🩺 Phase 3: Application Health (Self-Healing)
Ensuring the cluster knows when your app is ready or broken.

| Probe Type | Purpose | Command |
| :--- | :--- | :--- |
| Readiness | Controls traffic flow | `oc set probe deployment/myapp --readiness --get-url=http://:8080/health --initial-delay-seconds=5` |
| Liveness | Restarts "dead" pods | `oc set probe deployment/myapp --liveness --get-url=http://:8080/health --initial-delay-seconds=15` |

### 💾 Phase 4: Persistent Storage
Ensuring data survives pod restarts and deletions.

**Storage Commands**
* Check Storage Classes: `oc get sc`
* Add PVC to Deployment:
```bash
oc set volume deployment/myapp --add \
    --name=myapp-storage \
    --type=pvc \
    --claim-name=myapp-pvc \
    --claim-size=1Gi \
    --mount-path=/data
```

**Verification Workflow**
* Check Mount: `oc exec <pod> -- df -h /data`
* Write Data: `oc exec <pod> -- sh -c "echo 'hello' > /data/test.txt"`
* Delete Pod: `oc delete pod <pod>`
* Verify Persistence: `oc exec <new-pod> -- cat /data/test.txt`

### ⚖️ Phase 5: Resource Management
Setting the "Quality of Service" for cluster stability.

| Resource Type | Definition | Command Flag |
| :--- | :--- | :--- |
| Request | Minimum guaranteed (Reservation) | `--requests=cpu=10m,memory=64Mi` |
| Limit | Hard ceiling (Safety rail) | `--limits=cpu=200m,memory=512Mi` |

**Full Command:**
```bash
oc set resources deployment/myapp --limits=cpu=200m,memory=512Mi --requests=cpu=10m,memory=64Mi
```

### 🔍 Troubleshooting Toolbox
* **Pod Details:** `oc describe pod <pod_name>`
* **Recent Events:** `oc get events --sort-by='.lastTimestamp'`
* **Live Metrics:** `oc adm top pods`
* **Check Env Vars:** `oc exec <pod> -- env | grep <KEY>`

## Day 3: Advanced Pod Architecture & Multi-Container Patterns
**Focus:** Advanced Pod Architecture, Security Identities, and Multi-Container Patterns

### 🏗️ Phase 8: The Initialization Layer (Init Containers)
**Goal:** Execute setup logic before the main application starts.
**Implementation:** Added an `init-setup` container using the `busybox` image.
**Action:** Successfully created `/mnt/data/version.txt` on the persistent volume.
**Lesson:** Init containers must exit (Exit Code 0) before the main container starts.

### 🔐 Phase 9: Service Accounts & RBAC (Pod Identity)
**Goal:** Grant the Pod permissions to talk to the OpenShift API.
**Implementation:** Created the `visitor-admin` Service Account and bound it to the `view` Role.
**Verification:** Used `curl` with the projected token at `/var/run/secrets/kubernetes.io/serviceaccount/token` to list pods in the namespace.
**Insight:** Target the specific container (e.g., `-c visitor-app`) when executing commands if the default container lacks the necessary tools like `curl`.

### 🛰️ Phase 10: The Sidecar Pattern (Multi-Container Pods)
**Goal:** Add secondary functionality (logging) without modifying the main app code.
**Implementation:** Added `sidecar-logger` to run `tail -f /mnt/data/history.txt`.
**Shared Resources:** Both containers share the same network (localhost) and the same log-pvc mount.
**Verification:** `oc logs <pod> -c sidecar-logger` shows the real-time stream of the history log.

### 🔍 Troubleshooting Highlights (The "Architect's Notebook")

| Issue | Root Cause | Resolution |
| :--- | :--- | :--- |
| Multi-Attach Error | `gp3` (RWO) volume locked by a terminating Pod on a different node. | Scaled deployment to 0, then back to 1 to clear the volume lock. |
| 403 Forbidden API | Local shell expanded `$(cat token)` on the host instead of inside the Pod. | Wrapped the `oc exec` command in single quotes (`' '`) to ensure execution inside the container. |
| command not found (127) | Tried running `curl` inside the `busybox` sidecar which lacks that binary. | Used `-c visitor-app` to target the Python-based container which includes networking tools. |

## Day 4: CI/CD Automation & Image Promotion
**Focus:** CI/CD Automation, Quality Guardrails, and Image Promotion

### 🏗️ Phase 11: Post-Commit Hooks (The Quality Guardrail)
**Goal:** Execute logic inside your new image before it is pushed to the registry. If the hook fails, the image is discarded.
**Key Concepts:**
*   **Gatekeeping:** Prevents syntax errors or failed tests from entering the ImageStream.
*   **Context:** Runs inside the newly built container but before it is "finalized."
*   **Exit Codes:** A non-zero exit code (failure) stops the build process immediately.

**Commands:**
```bash
# Add a Python syntax check as a post-commit hook
oc set build-hook bc/visitor-app --post-commit --command -- python3 -m py_compile visitor_log.py

# Verify the hook is configured in the BuildConfig
oc describe bc visitor-app | grep -A 3 "Post Commit"
```

### 🤖 Phase 12: Build & Deployment Triggers
**Goal:** Enable OpenShift to react automatically to changes in the environment.
**Key Concepts:**
*   **ImageChange:** Triggers a new deployment rollout whenever the specified ImageStreamTag is updated (e.g., after a successful build).
*   **ConfigChange:** Triggers a rollout whenever the Deployment template itself changes (e.g., a new Environment Variable or Secret is added).

**Commands:**
```bash
# View all current triggers for a deployment
oc set triggers deployment/visitor-app

# Manually add an ImageChange trigger
oc set triggers deployment/visitor-app --from-image=visitor-app:latest -c visitor-app
```

### ❄️ Phase 13: ImageStreams & Tagging (Promotion)
**Goal:** Move an image from a "latest/development" state to a "stable/production" state by changing its tag pointer.
**Key Concepts:**
*   **Immutability:** By pointing a Deployment to a `:prod` tag instead of `:latest`, you ensure the app only updates when you explicitly "promote" a new image hash to that tag.
*   **Tagging:** Creating a pointer in an ImageStream to a specific image hash.

**Commands:**
```bash
# Promote the 'latest' image to 'prod'
oc tag visitor-app:latest visitor-app:prod

# Update deployment to use the 'prod' tag (Frozen version)
oc set image deployment/visitor-app visitor-app=$(oc get is visitor-app -o jsonpath='{.status.dockerImageRepository}'):prod

# Update the trigger to watch 'prod' instead of 'latest'
oc set triggers deployment/visitor-app --from-image=visitor-app:prod -c visitor-app --auto
```

### 🌐 Phase 14: Internal Networking & Service Discovery
**Goal:** Understanding how components communicate inside the cluster without external routes.
**Key Concepts:**
*   **Service DNS:** The internal address format: `<service>.<namespace>.svc.cluster.local`.
*   **Edge Termination:** SSL/TLS is handled by the OpenShift Router (the edge), while traffic to the pod is plain HTTP.

**Commands:**
```bash
# Create a secure Edge-terminated route
oc create route edge visitor-secure --service=visitor-app

# Verify internal connectivity (Testing the DNS)
oc exec <pod_name> -- curl http://visitor-app.dubeyhari76-dev.svc.cluster.local:8080/health
```

### 🔍 Troubleshooting Recap (Day 4)

| Problem | Root Cause | Resolution |
| :--- | :--- | :--- |
| Build Error: Step 2/2 | Post-commit hook failed due to code syntax error. | Fix local code, ensure successful local linting, and restart build. |
| App not updating after build | Deployment is watching a static tag (like `:prod`) instead of `:latest`. | Manually promote the image using `oc tag` or switch trigger to `:latest`. |
| 403 Forbidden on API | Service Account lacks sufficient Roles (e.g., `view`). | Use `oc policy add-role-to-user view -z <sa-name>`. |