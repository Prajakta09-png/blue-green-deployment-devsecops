# SecureGitOps Implementation Notes

## Project Overview

SecureGitOps is a DevSecOps and GitOps-based blue-green deployment platform built on Kubernetes.

It automates the flow from code commit to secure container build, vulnerability scanning, DockerHub image push, GitOps deployment with ArgoCD, monitoring with Prometheus and Grafana, centralized logging with Loki and Promtail, and email notification through GitHub Actions.

## Final Architecture Flow

Developer pushes code to GitHub
-> GitHub Actions pipeline starts
-> Unit tests run using pytest
-> Docker image is built
-> Trivy scans the Docker image
-> Image is pushed to DockerHub
-> GitHub Actions updates Kubernetes manifests with new image SHA tag
-> Updated manifests are pushed to GitHub
-> ArgoCD detects Git change
-> ArgoCD syncs the application to Kubernetes
-> Application runs using Blue-Green deployment
-> Prometheus collects metrics
-> Grafana visualizes metrics
-> Promtail collects pod logs
-> Loki stores centralized logs
-> Email notification is sent

## Technologies Used

- Python Flask: Demo web application
- Pytest: Unit testing
- Docker: Containerization
- DockerHub: Image registry
- GitHub Actions: CI/CD automation
- Trivy: Vulnerability scanning
- Kubernetes: Container orchestration
- Minikube: Local Kubernetes cluster
- ArgoCD: GitOps deployment and self-healing
- Prometheus: Metrics collection
- Grafana: Metrics and log visualization
- Loki: Centralized log storage
- Promtail: Kubernetes pod log collection

## Application Details

The application exposes these endpoints:

- /
- /health
- /version

The /health endpoint verifies that the app is running.

The /version endpoint verifies whether the live deployment is blue or green.

## CI/CD Workflow

GitHub Actions workflow file:

.github/workflows/ci-cd.yml

The workflow performs:

1. Checkout source code
2. Set up Python
3. Install dependencies
4. Run pytest unit tests
5. Build Docker image
6. Scan Docker image using Trivy
7. Push Docker image to DockerHub
8. Update Kubernetes manifests with commit SHA image tag
9. Push updated manifests to GitHub
10. Send email notification after success or failure

Docker image:

itisscdac/devsecops-flask-app

Tags used:

- itisscdac/devsecops-flask-app:<commit-sha>
- itisscdac/devsecops-flask-app:latest

Using commit SHA makes deployments traceable to a specific Git commit.

## GitOps CD with ArgoCD

ArgoCD is used for GitOps-based continuous deployment.

GitHub Actions updates the Kubernetes manifest image tag after a successful build. ArgoCD detects that Git change and deploys the updated manifest to the Kubernetes cluster.

ArgoCD provides:

- Automated sync
- Self-healing
- Drift correction
- Git as the source of truth

ArgoCD application name:

blue-green-devsecops-app

Expected status:

Synced and Healthy

## Blue-Green Deployment

The project uses two Kubernetes deployments:

- flask-app-blue
- flask-app-green

The Kubernetes Service controls live traffic using the version selector.

For blue deployment:

version: blue

For green deployment:

version: green

Rollback is done by switching the service selector back to the previous version.

## Kubernetes Security Hardening

Security hardening is implemented directly in Kubernetes deployment manifests.

Controls implemented:

- Run as non-root
- Disable privilege escalation
- Drop all Linux capabilities
- Read-only root filesystem
- CPU and memory requests
- CPU and memory limits

This improves container security and prevents uncontrolled resource usage.

## Trivy Security Scanning

Trivy scans the Docker image in the CI pipeline.

The pipeline fails if HIGH or CRITICAL vulnerabilities are found.

This acts as a security gate before deployment.

## Monitoring

Prometheus and Grafana are used for monitoring.

Namespace:

monitoring

Components:

- prometheus-server
- prometheus-kube-state-metrics
- prometheus-node-exporter
- grafana

Grafana Prometheus data source URL:

http://prometheus-server.monitoring.svc.cluster.local

Proof query used in Grafana Explore:

up

A value of 1 means the target is healthy and being scraped.

## Centralized Logging

Loki and Promtail are used for logging.

Namespace:

logging

Components:

- loki
- loki-promtail

Grafana Loki data source URL:

http://loki.logging.svc.cluster.local:3100

Proof query used in Grafana Explore:

{namespace="devsecops-platform", app="flask-app"}

This shows logs from the Flask application pods.

Example logs collected:

- GET /health HTTP/1.1 200
- GET /version HTTP/1.1 200

## Email Notification

GitHub Actions sends email after pipeline success or failure.

Secrets used:

- DOCKER_USERNAME
- DOCKER_PASSWORD
- MAIL_USERNAME
- MAIL_PASSWORD
- NOTIFICATION_EMAIL

The email notification confirms pipeline status, branch, commit SHA, and Docker image tag.

## Kyverno Note

Kyverno was tested as an optional Kubernetes policy enforcement add-on.

However, it overloaded the local Minikube environment and caused API server instability. Therefore, Kyverno was removed and documented as a future enhancement.

Security hardening is already implemented directly in the Kubernetes manifests.

## Final Verification Commands

Check ArgoCD:

kubectl get applications -n argocd

Check application:

kubectl get pods -n devsecops-platform
curl http://192.168.49.2:30080/health
curl http://192.168.49.2:30080/version

Check monitoring:

kubectl get pods -n monitoring

Check logging:

kubectl get pods -n logging

## Screenshots to Include

Recommended screenshots:

1. Successful GitHub Actions workflow
2. Email notification received
3. DockerHub image repository
4. ArgoCD Synced and Healthy
5. Blue and Green Kubernetes pods running
6. /health and /version curl output
7. Grafana Prometheus query result
8. Grafana Loki logs result
9. Trivy scan result

## Interview Explanation

SecureGitOps is a DevSecOps project that automates secure application delivery to Kubernetes.

When code is pushed to GitHub, GitHub Actions runs tests, builds a Docker image, scans it using Trivy, and pushes it to DockerHub. The workflow then updates Kubernetes manifests with the new image SHA tag and pushes the change back to GitHub.

ArgoCD watches the repository and automatically syncs the updated manifests to Kubernetes. This makes Git the source of truth and provides GitOps-based continuous deployment.

The application uses a blue-green deployment strategy where traffic can be switched between Blue and Green versions using the Kubernetes Service selector. This allows safer releases and quick rollback.

Prometheus and Grafana provide monitoring, while Loki and Promtail provide centralized logging. Email notifications are sent after pipeline success or failure.

## Project Status

Completed:

- Flask application
- Dockerization
- Pytest unit testing
- GitHub Actions CI/CD
- Trivy image scanning
- DockerHub image push
- GitOps manifest update
- ArgoCD sync
- ArgoCD self-healing
- Blue-green deployment
- Rollback testing
- Kubernetes security hardening
- Prometheus monitoring
- Grafana visualization
- Loki logging
- Promtail log collection
- Email notification

Future enhancements:

- Kyverno policy enforcement on larger cluster
- Terraform infrastructure provisioning
- Ingress controller
- TLS with cert-manager
- Horizontal Pod Autoscaler
- Slack notification
- Canary deployment
