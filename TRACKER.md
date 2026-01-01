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