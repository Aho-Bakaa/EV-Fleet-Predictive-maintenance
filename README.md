# EV Fleet Predictive Maintenance API

FastAPI backend for EV battery predictive maintenance.
The service predicts battery SOH, RUL, and thermal runaway risk, then returns actionable maintenance alerts.

## Highlights

- Multi-target battery diagnostics (SOH, RUL, thermal risk)
- Structured operational alerts (`OK`, `WARNING`, `URGENT`, `CRITICAL`)
- OpenAPI docs via Swagger (`/docs`) and ReDoc (`/redoc`)
- Container-ready deployment with Docker

## Tech Stack

- Python 3.9+
- FastAPI + Pydantic
- scikit-learn, joblib, pandas, numpy
- Docker

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
|   |-- analysis/              # Curated startup-facing analysis artifacts
|   `-- assets/                # Supporting plot assets
|-- test_inference.py          # Local inference smoke test
|-- requirements.txt
`-- Dockerfile
```

## Quick Start (Local)

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure all required `.pkl` model/scaler files exist in `models/` with the exact names configured in `app/config.py`.
4. Start the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

5. Open docs:
- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## Run with Docker

```bash
docker build -t ev-fleet-predictive-maintenance .
docker run --rm -p 8000:8000 ev-fleet-predictive-maintenance
```

## API Endpoints

- `GET /` - service metadata and endpoint map
- `GET /health` - service health check
- `GET /model/info` - model metadata and threshold values
- `POST /predict` - predictive maintenance inference

### Example Prediction Request

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  --data @app/sample_request.json
```

## Analysis Artifacts (Curated)

- Synthetic data assessment and relevance filter:
  `docs/analysis/synthetic_data_assessment.md`
- Startup critique:
  `docs/analysis/startup_critique.md`
- Correlation visuals:
  `docs/assets/correlations/`
- Supporting report and metrics table:
  `docs/analysis/Report.pdf`, `docs/analysis/model_training_results.csv`

## Troubleshooting

- Missing feature errors:
  Verify your payload includes all required `FEATURE_COLUMNS` from `app/config.py`.
- Model file errors:
  Check that all configured model/scaler files exist under `models/`.
- `503` from `/predict`:
  Models may still be loading or failed during startup.

## Production Notes

- Add authentication and rate limiting before public exposure.
- Keep model artifact versions aligned with `MODEL_VERSION`.
- Current analysis artifacts are based on synthetic fleet data generation and should be presented as MVP validation, not production-grade field validation.
