# Predictive Maintenance MLOps Pipeline

A production-ready MLOps project for predicting engine failures 30 days in advance using sensor telemetry data (predictive maintenence). This is a complete end-to-end machine learning system with training, serving, monitoring, and deployment infrastructure.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Project](#running-the-project)
- [Docker Setup](#docker-setup)
- [Kubernetes Deployment](#kubernetes-deployment)
- [API Documentation](#api-documentation)
- [Monitoring & Observability](#monitoring--observability)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)

## Features

✅ **Machine Learning**
- Predictive maintenance model using RandomForest
- Time-series feature engineering (24 timesteps × 6 sensors)
- Binary classification (Normal/Failure)
- ~95% accuracy on test data

✅ **API Service**
- FastAPI-based REST API
- Interactive documentation (Swagger/ReDoc)
- Request/response validation with Pydantic
- Health checks and monitoring endpoints

✅ **Model Management**
- MLflow for experiment tracking
- Model versioning and registry
- Automated model persistence
- Model validation and health checks

✅ **Monitoring & Observability**
- Prometheus metrics collection
- Data drift detection (Evidently)
- Grafana dashboards
- Comprehensive logging

✅ **Infrastructure**
- Docker containerization
- Kubernetes deployment manifests
- Docker Compose for local development
- Horizontal Pod Autoscaler (HPA)
- CI/CD with GitHub Actions

✅ **Testing**
- Unit tests for model and data
- API endpoint tests
- Data validation tests
- pytest with coverage reports

## Tech Stack

### Core
- **Language**: Python 3.10+
- **API Framework**: FastAPI + Uvicorn
- **ML Framework**: Scikit-Learn
- **Data**: Pandas, NumPy

### Infrastructure & Orchestration
- **Containerization**: Docker
- **Orchestration**: Kubernetes (Minikube/EKS)
- **Workflow**: Apache Airflow
- **Server**: Uvicorn

### ML & Monitoring
- **Experiment Tracking**: MLflow
- **Monitoring**: Prometheus + Grafana
- **Drift Detection**: Evidently
- **Data Versioning**: DVC

### Testing & Quality
- **Testing**: Pytest
- **Linting**: Flake8
- **Formatting**: Black, isort
- **Type Checking**: mypy

### CI/CD
- **Version Control**: GitHub
- **CI/CD**: GitHub Actions
- **Container Registry**: Docker Hub

## Quick Start

### Prerequisites
- Python 3.10+
- Docker (optional, for containerized setup)
- Git

### 5-Minute Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd predictive-maintenance

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate training data
python src/data/download_data.py

# 4. Train the model
python src/model/train.py

# 5. Run the API server
python src/api/app.py
```

The API will be available at **http://localhost:8000**
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Project Structure

```
predictive-maintenance/
├── src/                          # Source code
│   ├── api/                      # FastAPI application
│   │   └── app.py               # Main API endpoints
│   ├── model/                    # ML model code
│   │   ├── train.py             # Training pipeline
│   │   └── validator.py         # Model validation
│   ├── data/                     # Data processing
│   │   ├── download_data.py     # Data generation
│   │   └── validation.py        # Data validation
│   ├── monitoring/               # Monitoring utilities
│   │   ├── prometheus_metrics.py # Metrics collection
│   │   └── drift_detector.py    # Drift detection
│   ├── config.py                # Configuration management
│   └── logger.py                # Logging setup
│
├── tests/                        # Test suite
│   ├── test_model.py            # Model tests
│   ├── test_data.py             # Data validation tests
│   ├── test_api_local.py        # API endpoint tests
│   └── conftest.py              # Pytest fixtures
│
├── k8s/                          # Kubernetes manifests
│   ├── deployment.yaml          # Deployment config
│   ├── service.yaml             # Service config
│   ├── configmap.yaml           # ConfigMap
│   ├── hpa.yaml                 # Auto-scaler
│   └── ingress.yaml             # Ingress
│
├── monitoring/                   # Monitoring configs
│   └── prometheus.yml           # Prometheus config
│
├── docs/                         # Documentation
│   ├── API.md                   # API documentation
│   ├── DEPLOYMENT.md            # Deployment guide
│   ├── DEVELOPMENT.md           # Development guide
│   └── ARCHITECTURE.md          # Architecture docs
│
├── scripts/                      # Utility scripts
│   ├── setup.sh                 # Setup script
│   └── deploy.sh                # Deployment script
│
├── Dockerfile                    # Container definition
├── docker-compose.yml            # Local dev stack
├── Makefile                      # Common tasks
├── config.yaml                   # Application config
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Setup Instructions

### Option 1: Local Development (Recommended for Getting Started)

```bash
# 1. Clone repository
git clone <repo-url>
cd predictive-maintenance

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment template
cp .env.example .env

# 5. Create necessary directories
mkdir -p logs models data/raw data/processed

# 6. Generate data and train model
python src/data/download_data.py
python src/model/train.py
```

### Option 2: Using Docker Compose (Complete Stack)

```bash
# 1. Clone repository
git clone <repo-url>
cd predictive-maintenance

# 2. Start the stack
docker-compose up -d

# 3. Wait for services to be ready
docker-compose logs -f api
```

This starts:
- **API**: http://localhost:8000
- **MLflow**: http://localhost:5000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

### Option 3: Using Makefile (Automated)

```bash
# Clone and setup everything
make dev
make data
make train
make api
```

## Running the Project

### Generate Training Data
```bash
python src/data/download_data.py
```

### Train the Model
```bash
python src/model/train.py
```

### Run the API Server
```bash
# Development mode with auto-reload
python src/api/app.py

# Or with uvicorn directly
uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
```

### Run Tests
```bash
# All tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=src --cov-report=html

# Specific test file
pytest tests/test_api_local.py -v
```

### Run Linting & Formatting
```bash
# Format code
black src tests
isort src tests

# Check linting
flake8 src tests

# Type checking
mypy src
```

## Docker Setup

### Build Docker Image
```bash
docker build -t predictive-maintenance:latest .
```

### Run with Docker
```bash
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  predictive-maintenance:latest
```

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (1.20+)
- kubectl configured
- Models built and pushed to registry

### Deploy to Kubernetes
```bash
# Update image in deployment
sed -i 's|your-registry|your-actual-registry|g' k8s/deployment.yaml

# Apply manifests
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

# Verify deployment
kubectl get pods -l app=predictive-maintenance
kubectl get svc predictive-maintenance-service
```

### Access the Service
```bash
# Port forward
kubectl port-forward svc/predictive-maintenance-service 8000:8000

# API available at http://localhost:8000
```

## API Documentation

### Health Check
```bash
curl http://localhost:8000/health
```

### Make a Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @payload.json
```

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

For detailed API documentation, see [docs/API.md](docs/API.md)

## Monitoring & Observability

### MLflow
```bash
mlflow ui --host 0.0.0.0 --port 5000
```
Access at http://localhost:5000

### Prometheus
Access at http://localhost:9090 (if using docker-compose)

### Grafana
```
URL: http://localhost:3000
Username: admin
Password: admin
```

## Environment Variables

Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

Key variables:
```
ENV=development              # development or production
DEBUG=True                  # Enable/disable debug mode
API_PORT=8000              # API server port
MLFLOW_TRACKING_URI=http://localhost:5000
LOG_LEVEL=INFO             # INFO, DEBUG, WARNING, ERROR
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow
1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and add tests
3. Run linting: `make lint`
4. Run tests: `make test`
5. Format code: `make format`
6. Commit: `git commit -m "descriptive message"`
7. Push and create a Pull Request

## Troubleshooting

### Model Not Found Error
```
Error: Model or scaler not found! Run: python src/model/train.py
```
**Solution**: Train the model first using `python src/model/train.py`

### API Port Already in Use
```
Error: Address already in use
```
**Solution**: Change the port or kill the process on port 8000:
```bash
lsof -i :8000
kill -9 <PID>
```

### Docker Build Fails
```
Error: No such file or directory
```
**Solution**: Ensure you're in the `predictive-maintenance` directory:
```bash
cd predictive-maintenance
docker build -t predictive-maintenance:latest .
```

### Tests Failing
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Run tests with verbose output
pytest tests/ -v --tb=long

# Check test logs
cat logs/app.log
```

### Database Connection Issues
If using Kubernetes with database:
```bash
# Check database connectivity
kubectl exec <pod-name> -- mysql -h db -u user -p
```

### Permission Denied on Scripts
```bash
chmod +x scripts/setup.sh scripts/deploy.sh
```

## Performance Benchmarks

- **Average Latency**: 50-100ms per prediction
- **Throughput**: 100-200 predictions/second (single instance)
- **Model Accuracy**: ~95%
- **Training Time**: ~5-10 minutes
- **Inference Time**: ~50ms per request

## Resources

- [API Documentation](docs/API.md) - API endpoints and examples
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment
- [Development Guide](docs/DEVELOPMENT.md) - Local development
- [Architecture](docs/ARCHITECTURE.md) - System design
- [Contributing](CONTRIBUTING.md) - How to contribute
- [Changelog](CHANGELOG.md) - Version history

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## Support

For issues, questions, or suggestions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review [docs/](docs/) directory
3. Open an GitHub issue
4. Contact: [your-email@example.com]

## Acknowledgments

- Built with FastAPI, Scikit-Learn, and MLflow
- Monitoring powered by Prometheus and Grafana
- Kubernetes deployment support
- Community contributions welcome!

---

**Happy predicting! 🚀**
