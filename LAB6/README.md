# Cloud Runner Basic Lab — Modified Submission

> **Note:** This lab is based on the original Cloud Runner Basic Lab provided by the professor. I have made two modifications to the original instructions, which are described below. The core structure and learning objectives remain the same.

---

## Changes I Made

### Change 1: Replaced Google Container Registry (GCR) with Artifact Registry (AR)

In the original lab, the instructions use Google Container Registry (`gcr.io`) to store the Docker image. I updated this to use **Artifact Registry** instead, because GCR is being phased out by Google and Artifact Registry is now the officially recommended replacement. This affects Step 1 (enabling a different API), Step 3 (authentication and push commands), and the deploy step where the image URL is referenced.

The key difference in the image URL format is:
- **Original (GCR):** `gcr.io/YOUR_PROJECT_ID/hello-world`
- **Updated (AR):** `REGION-docker.pkg.dev/YOUR_PROJECT_ID/YOUR_REPOSITORY/hello-world`

### Change 2: Added a Step to Configure Concurrency and Memory Limits

The original lab deploys the service with default settings and moves straight to testing. I added a step after deployment to explicitly configure the concurrency limit and memory allocation using the `gcloud run services update` command. I felt this was a useful addition because it shows how to tune the service for real-world use, and it connects naturally to the monitoring and scaling concepts covered at the end of the lab.

---

## Step-by-Step Guide

### Step 1: Set Up Google Cloud Project

1. **Create a Google Cloud Project:**
   - Go to the **Google Cloud Console**.
   - Create a new project and give it a meaningful name (e.g., `cloud_runner_lab`).

2. **Enable Necessary APIs:**
   - In the Console, navigate to `APIs & Services > Library`.
   - Enable the **Cloud Run API** and the **Artifact Registry API**.
   *(Note: The original lab enables the Container Registry API here. I replaced it with the Artifact Registry API to match the updated workflow in Step 3.)*

---

### Step 2: Create and Containerize the Application

1. **Create a Simple Flask Application:**
   - Write a basic Flask application in Python to use as your project.


2. **Create a Dockerfile:**
   - In the same directory as your Flask app, create a Dockerfile to containerize the application.


3. **Build the Docker Image:**
   - Ensure Docker is running on your local machine.
   - In the terminal, navigate to the app's directory and build the Docker image:

```bash
docker build -t REGION-docker.pkg.dev/YOUR_PROJECT_ID/YOUR_REPOSITORY/hello-world .
```

> Replace `REGION` (e.g., `us-central1`), `YOUR_PROJECT_ID`, and `YOUR_REPOSITORY` with your actual values.

---

### Step 3: Push the Docker Image to Artifact Registry
*(This step replaces the original "Push to Container Registry" step.)*

1. **Create an Artifact Registry Repository:**
   - In the Console, navigate to `Artifact Registry > Repositories`.
   - Click **Create Repository**.
   - Set the format to **Docker**, choose a region (e.g., `us-central1`), and give it a name (e.g., `cloud-run-repo`).

2. **Authenticate with Artifact Registry:**
   - Configure Docker to authenticate with your Artifact Registry region:

```bash
gcloud auth configure-docker REGION-docker.pkg.dev
```

3. **Push the Docker Image:**
   - Push your Docker image to Artifact Registry:

```bash
docker push REGION-docker.pkg.dev/YOUR_PROJECT_ID/YOUR_REPOSITORY/hello-world
```

---

### Step 4: Deploy to Google Cloud Run

1. **Navigate to Cloud Run in Google Console:**
   - Go to the Cloud Run service in the Google Cloud Console.
   - Click **Create Service**.

2. **Configure the Deployment:**
   - Select **Deploy a container image** and choose the image you pushed to Artifact Registry.
   - Set the **Region** (e.g., `us-central1`) and provide a **Service name**.
   - For **Authentication**, select "Allow unauthenticated invocations" if you want the app to be publicly accessible.

3. **Deploy the Application:**
   - Click **Create** to deploy the service. This process may take a few minutes.
   - Once deployed, Cloud Run will provide a URL for your application.

---

### Step 5: Configure Concurrency and Memory Limits
*(This is a new step I added that was not in the original lab.)*

Before testing, I configured the concurrency and memory settings for the deployed service. This can be done via the CLI:

```bash
gcloud run services update YOUR_SERVICE_NAME \
  --concurrency 80 \
  --memory 256Mi \
  --region REGION
```

- `--concurrency` sets how many requests a single container instance handles at once. Lowering this causes Cloud Run to spin up more instances under load, which can improve performance but increases cost.
- `--memory` sets the memory available to each container instance. Choosing an appropriate value avoids both waste and out-of-memory errors under traffic.

I added this step because it ties directly into the monitoring and auto-scaling concepts in the final step, and gives a more complete picture of how to configure a Cloud Run service before putting it in front of real traffic.

---

### Step 6: Access and Test the Application

- Access the URL provided by Cloud Run to test your application.
- You should see the message **"Hello, World!"** displayed if everything is working correctly.

---

### Step 7: Monitor and Scale the Service

1. **Monitor Metrics:**
   - Use the Cloud Run Console to monitor various metrics such as request count, response latency, and memory usage.
   - These metrics help you understand traffic and performance patterns.

2. **Auto-Scaling:**
   - Cloud Run automatically scales your service based on incoming traffic.
   - You can configure the minimum and maximum number of instances if needed to control scaling.

---

## Conclusion

In my modified version, I additionally:
- Used **Artifact Registry** instead of Container Registry, reflecting Google's current recommended approach.
- Configured **concurrency and memory limits** after deployment to better understand how Cloud Run manages resources and scales under load.
