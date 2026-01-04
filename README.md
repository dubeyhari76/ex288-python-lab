# OpenShift Python Lab

## Step 0: Prerequisites

Ensure the OpenShift CLI (`oc`) is installed and available in your shell's PATH.

## Step 1: Log in to your Cluster

1. Go to the Red Hat Developer Sandbox.
2. Click "OpenShift Console".
3. In the top right, click your name -> "Copy Login Command".
4. Paste that command into your local terminal.

## Step 2: Create the Build (The Magic Command)

Run the following command. Replace `YOUR_GITHUB_URL` with the repo you just created.

```bash
oc new-app python~https://github.com/YOUR_USERNAME/ex288-python-lab --name=myapp
```

### Breakdown of the command (Exam Logic):

*   `python~`: This tells OpenShift explicitly "Use the Python Builder Image." If you omit this, OpenShift tries to guess the language (which is slower and sometimes wrong).
*   `--name=myapp`: This labels all created resources (Service, Deployment, Pods) with `app=myapp`.

## Step 3: Watch the Build

OpenShift is now cloning your repo and compiling the image. Watch the logs:

```bash
oc logs -f buildconfig/myapp
```

**Success Indicator:** You should see "Pushing image..." and "Push successful".

## Phase 3: Expose and Verify

By default, your app is running inside the cluster but is not accessible from the internet. You need a Route.

### Step 1: Expose the Service

```bash
oc expose service/myapp
```

### Step 2: Get the URL

```bash
oc get route myapp
```

Copy the URL under the `HOST/PORT` column and paste it into your browser.

**Expected Result:** You should see text like: `Hello! Served from Pod: myapp-1-g4kz2`

## Troubleshooting Drill (The "Exam" Part)

If that worked, congratulations! You just did an S2I build. Now, answer this question to check your understanding:

**Question:** OpenShift automatically detected that it needed to run `pip install -r requirements.txt`. How did it know to do that?

*   [ ] It is hardcoded in OpenShift.
*   [ ] The "Python Builder Image" contains a script named assemble that looks for that specific filename.
*   [ ] The `oc new-app` command scanned your local directory before sending the request.


# Retrospective

## Day 1: Basic Pod and Service. 

## Day 2: Persistence (PVC) and Health Probes. 

## Day 3: Multi-container Pods (Init/Sidecar) and Service Accounts. 

## Day 4: Automated Build Hooks and Image Promotion.