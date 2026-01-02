# OpenShift Architect Tracker: Exercise EX288 🚀

## Day-01 (01/01/2026)

### 1. Build & Deployment 🏗️
* **Binary Build:** `oc start-build myapp --from-dir=. --follow`
* **Route Verification:** `oc describe route myapp`
* **Service Verification:** `oc describe svc myapp`

### 2. Configuration (ConfigMaps) ⚙️
* **Create ConfigMap:** `oc create configmap app-config --from-literal=GREETING=Namaste`
* **Link to Deployment:** `oc set env deployment/myapp --from=configmap/app-config`
* **View ConfigMap Details:** `oc get cm app-config -o yaml`
* **Replace ConfigMap Content:** `oc create configmap app-config --from-literal=GREETING="Radhey Radhey Ji" --dry-run=client -o yaml | oc replace -f -`
        
### 3. Debugging & Maintenance 🔍
* **Inspect Pod Environment:** `oc describe pod <pod_name>`
* **Verify Filesystem Code:** `oc exec <pod_name> -- cat app.py`
* **Check Internal Environment:** `oc exec <pod_name> -- env | grep GREETING`
* **Test Local App Response:** `oc exec <pod_name> -- curl -s localhost:8080`
* **Remove Specific Env Var:** `oc set env deployment/myapp GREETINGS-`

### 4. Lifecycle & Scaling 📈
* **Trigger Rolling Restart:** `oc rollout restart deployment/myapp`
* **Scale Replicas:** `oc scale deployment myapp --replicas=3`
* **Test Load Balancing:** `for i in {1..5}; do curl -s <route_url>; done`

## Day-02 (01/02/2026)

### Project: Python Health & Persistence App
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