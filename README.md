# EV Fleet Predictive Maintenance API

This repository contains the backend for an Intelligent EV Fleet Predictive Maintenance platform. The core objective is simple: help operations teams answer, "When does Vehicle X need attention?"

The system evolved from basic snapshot-style prediction into a vehicle- and time-aware pipeline that ingests telemetry, handles synthetic fleet generation when needed, and serves multi-target maintenance predictions through a FastAPI service.

## What The System Predicts

The API focuses on three battery-critical outputs: state of health (SOH), remaining useful life (RUL), and thermal runaway risk. The modeling is component-aware and designed for maintenance decision support rather than isolated benchmark scoring.

## Development Direction

During development, the project moved from broad correlation exploration to a tighter battery/component framing, with updated targets, feature engineering, and validation logic that preserves vehicle identity and temporal behavior.

## Repository Scope

This codebase includes the production-facing backend inference service, model artifacts required by the API, and supporting project files used to run and evaluate the service.

## Tech Stack

Python 3.9+, FastAPI, Pydantic, scikit-learn, joblib, pandas, numpy, and Docker.

## Repository Layout

```text
.
|-- app/
|   |-- main.py                # API routes and server lifecycle
|   |-- inference.py           # Model loading and prediction pipeline
|   |-- config.py              # Paths, feature list, and alert thresholds
|   |-- schemas.py             # Request/response schemas
|   `-- sample_request.json    # Example request payload
|-- models/                    # Serialized model and scaler artifacts (.pkl)
|-- docs/
|   `-- analysis/
|       `-- Report.pdf         # Findings, methodology, and approach
|-- test_inference.py          # Local inference smoke test
|-- requirements.txt
`-- Dockerfile
```

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open API docs at `http://localhost:8000/docs` or `http://localhost:8000/redoc`.

## Docker

```bash
docker build -t ev-fleet-predictive-maintenance .
docker run --rm -p 8000:8000 ev-fleet-predictive-maintenance
```

## API Endpoints

- `GET /` service metadata and endpoint map
- `GET /health` health check
- `GET /model/info` model metadata and thresholds
- `POST /predict` predictive maintenance inference

## Project Report

Detailed findings, modeling decisions, and project approach are documented in:
[EV Fleet Project Report](docs/analysis/Report.pdf)
