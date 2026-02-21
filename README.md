EV Predictive Maintenance Backend
Overview: 
This repository provides the backend API for an EV fleet predictive maintenance system. It enables real-time battery health prediction, risk assessment, and actionable maintenance alerts using pre-trained machine learning models.

Built with: FastAPI, Python 3.9, joblib, Docker

Models: SOH (State of Health), Battery RUL (Remaining Useful Life), Thermal Runaway Risk

Main Features

Robust REST API for vehicle data prediction

Scalable structure for containerized/cloud deployment

Swagger UI auto-documentation (/docs)

Configurable thresholds for actionable alerts

Easily extendable to support more targets/metrics

1. Prerequisites
   
Python 3.9 (recommended)
Docker Desktop (optional for containerization, recommended)

2. Install Dependencies

pip install -r requirements.txt

4. Prepare Model Files
   
Place all .pkl files for models and scalers in the models/ directory.
Ensure files are named exactly as referenced in config.py.

Troubleshooting
Missing feature error:
Double-check config.py and the sample_request.json to ensure all expected features are present and correctly ordered.

Model file not found:
Ensure all .pkl files are in models/.




Use Docker for deployment on cloud platforms like AWS/GCP/Render.

API can be scaled horizontally using Docker Compose.
