# Predictive Maintenance MLOps Pipeline

## Business Problem
Predict jet engine failures 30 days in advance using sensor data.

## Tech Stack
- **Infrastructure**: Minikube (local K8s) + Docker
- **Orchestration**: Airflow + Kubeflow
- **ML**: MLflow + Scikit-Learn
- **Monitoring**: Evidently (drift) + Prometheus + Grafana
- **CI/CD**: GitHub Actions

## Quick Start
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Minikube
minikube start --cpus=4 --memory=8192

# 3. Run training
python src/model/train.py

# 4. Start MLflow
mlflow ui --host 0.0.0.0 --port 5000
```

## Architecture
[To be added]
