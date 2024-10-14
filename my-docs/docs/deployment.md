# Deployment

## Introduction
To bring the Campaign Analytics Platform from a local environment to production, a well-planned deployment strategy is essential. The goal is to ensure the application is scalable, highly available, and easily maintainable. This document outlines the approach for deploying the application to Google Cloud Platform (GCP) and the CI/CD steps needed to automate the deployment whenever code changes are merged to the production branch.

## Deployment Approach
For deploying the FastAPI application to production, we can use **Google Kubernetes Engine (GKE)** along with other Google Cloud services. The deployment strategy includes:

1. **Containerization**: The application is containerized using Docker, which allows for consistent environments across development, testing, and production.

2. **Kubernetes**: Google Kubernetes Engine (GKE) is used to manage the application containers, providing a scalable and resilient deployment. Kubernetes helps in load balancing, scaling, and handling failures automatically.

3. **Database Setup**: The PostgreSQL database can be hosted using **Cloud SQL**, a fully managed database service provided by Google Cloud, which ensures reliability and ease of maintenance.

4. **Load Balancer**: A **Cloud Load Balancer** can be used to distribute traffic among multiple replicas of the application to ensure high availability.

## Steps to Deploy on Google Cloud
1. **Dockerize the Application**: Create a Docker image of the FastAPI application.
   ```bash
   docker build -t campaign-analytics .
   ```

2. **Push Docker Image to Google Container Registry (GCR)**:
   ```bash
   docker tag campaign-analytics gcr.io/<gcp-project-id>/campaign-analytics
   docker push gcr.io/<gcp-project-id>/campaign-analytics
   ```

3. **Create GKE Cluster**:
   - Use Google Cloud Console or CLI to create a GKE cluster.
   ```bash
   gcloud container clusters create campaign-cluster --num-nodes=3
   ```

4. **Deploy Application on GKE**:
   - Create a Kubernetes deployment YAML file (`deployment.yaml`) that defines the deployment for the application.
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: campaign-analytics-deployment
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: campaign-analytics
     template:
       metadata:
         labels:
           app: campaign-analytics
       spec:
         containers:
         - name: campaign-analytics
           image: gcr.io/<gcp-project-id>/campaign-analytics
           ports:
           - containerPort: 8000
   ```
   - Apply the deployment.
   ```bash
   kubectl apply -f deployment.yaml
   ```

5. **Expose the Application**:
   - Create a service to expose the application.
   ```bash
   kubectl expose deployment campaign-analytics-deployment --type=LoadBalancer --port 80 --target-port 8000
   ```

6. **Database Configuration**:
   - Set up a Cloud SQL instance for PostgreSQL and connect it to the GKE cluster by configuring the necessary connection details and credentials.

## CI/CD Pipeline
To automate the deployment of the application to production whenever changes are merged to the production branch, we can use **GitHub Actions** or **GitLab CI/CD**.

### CI/CD Pipeline Steps
1. **Build Stage**:
   - Triggered when changes are pushed to the production branch.
   - The Docker image is built for the latest version of the application.
   ```yaml
   - name: Build Docker Image
     run: docker build -t campaign-analytics .
   ```

2. **Push Stage**:
   - Push the Docker image to Google Container Registry (GCR).
   ```yaml
   - name: Push to Google Container Registry
     run: |
       docker tag campaign-analytics gcr.io/${{ secrets.GCP_PROJECT_ID }}/campaign-analytics
       docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/campaign-analytics
   ```

3. **Deploy Stage**:
   - Use `kubectl` to apply the Kubernetes manifests to the GKE cluster, deploying the updated application.
   ```yaml
   - name: Set up Kubeconfig
     uses: azure/setup-kubectl@v1
     with:
       version: 'v1.20.0'
   - name: Deploy to GKE
     run: kubectl apply -f deployment.yaml
   ```

### CI/CD Pipeline Example (GitHub Actions)
Below is an example GitHub Actions workflow file (`.github/workflows/deploy.yml`) for automating the deployment process:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - production

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Code
      uses: actions/checkout@v2

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v1

    - name: Build Docker Image
      run: docker build -t campaign-analytics .

    - name: Authenticate to Google Cloud
      uses: google-github-actions/auth@v0
      with:
        credentials_json: '${{ secrets.GCP_SA_KEY }}'

    - name: Push to Google Container Registry
      run: |
        docker tag campaign-analytics gcr.io/${{ secrets.GCP_PROJECT_ID }}/campaign-analytics
        docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/campaign-analytics

    - name: Set up Kubeconfig
      uses: azure/setup-kubectl@v1
      with:
        version: 'v1.20.0'

    - name: Deploy to GKE
      run: kubectl apply -f deployment.yaml
```

## Key Points
- **Scalability**: Using GKE allows for automatic scaling of application instances based on demand.
- **High Availability**: The application is deployed across multiple nodes to ensure high availability and reliability.
- **Automation**: CI/CD ensures that every change is automatically tested and deployed, reducing manual intervention and improving efficiency.

## Conclusion
Deploying the Campaign Analytics Platform to production involves using Google Kubernetes Engine for scalability, Cloud SQL for managed database services, and a CI/CD pipeline for automated deployments. This approach ensures that the application is reliable, easily maintainable, and capable of handling production traffic efficiently.

