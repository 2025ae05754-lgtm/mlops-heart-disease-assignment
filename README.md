# Cardio MLOps Platform

End-to-end heart disease risk prediction with reproducible training, a FastAPI inference service, Prometheus metrics, Docker, Kubernetes manifests, and CI.

## Quick start

```bash
python -m venv .venv
.venv\\Scripts\\activate  # Windows
pip install -r requirements.txt
python -m src.train
python -m pytest -q
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for the interactive API. `POST /predict` accepts the 13 Cleveland dataset features. `GET /health` and `GET /metrics` support probes and monitoring.

The assignment report and requirement checklist are in [`REPORT.md`](REPORT.md).

## Dataset

The complete UCI Heart Disease archive is included under `data/raw/heart-disease/`,
including the Cleveland, Hungarian, Switzerland, and VA datasets, metadata, and
cost files. The pipeline uses `data/raw/processed.cleveland.data` by default.

## Deployment

Build with `docker build -t cardiac-risk-api .`, run with `docker compose up --build`, or apply the manifests in `k8s/`. The included pipeline trains, tests, and builds the container on pushes and pull requests.

This project is educational and is not a medical diagnosis system. Predictions require clinical review.
