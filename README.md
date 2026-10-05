# Kubelab

Kubelab is a hands-on Kubernetes lab project built to demonstrate container orchestration, persistent storage, service networking, ingress routing, application configuration, and infrastructure practices using a small stateful web application.

## Architecture

```text
Browser
   |
   v
Traefik Ingress
   |
   v
kubelab-api Service
   |
   v
FastAPI Pod
   |
   v
PostgreSQL Service
   |
   v
PostgreSQL Pod
   |
   v
PersistentVolumeClaim
   |
   v
PersistentVolume
```

## Current Features

- Kubernetes deployment using k3s
- Containerized FastAPI application
- PostgreSQL database running in Kubernetes
- Persistent PostgreSQL storage using PVC/PV
- Kubernetes Services for application and database networking
- Traefik Ingress for browser access
- ConfigMap-based application configuration
- Kubernetes Secret for database credentials
- Readiness and liveness probes
- CPU and memory requests/limits
- REST API for creating and retrieving customers
- Browser-based customer management UI
- Rolling application deployments
- Persistent data across PostgreSQL Pod replacement

## Technology Stack

- Kubernetes / k3s
- Docker
- containerd
- FastAPI
- Python
- PostgreSQL
- Traefik
- HTML / JavaScript
- Git / GitHub

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Application health check |
| GET | `/environment` | Displays the configured application environment |
| GET | `/customers` | Retrieves customers from PostgreSQL |
| POST | `/customers` | Creates a customer |
| GET | `/ui` | Browser-based customer interface |

## Project Structure

```text
kubelab/
├── app/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── k8s/
    ├── configmap.yaml
    ├── deployment.yaml
    ├── ingress.yaml
    ├── namespace.yaml
    ├── postgres-service.yaml
    ├── postgres.yaml
    ├── pvc.yaml
    ├── secret.yaml
    └── service.yaml
```

## Planned Improvements

- Prometheus metrics collection
- Grafana dashboards
- CI/CD pipeline
- Automated container image publishing
- Helm packaging
- Horizontal Pod Autoscaling
- GitOps deployment workflow

## Purpose

This project is intentionally small at the application layer. Its primary purpose is to provide a practical environment for building and demonstrating Kubernetes and infrastructure engineering skills.
