# VAJRA Project Memory

## Current Phase
Project Complete - Production Prototype Ready.

## Completed Work
- [x] Phase 0: Project Foundation (Structure, Config, Logger).
- [x] Phase 1-2: Data Ingestion & Alignment (Real NWP loaders, Regridding).
- [x] Phase 3: Forecast Verification (Bust labeling logic).
- [x] Phase 4: Feature Engineering (Ensemble spread, Regimes).
- [x] Phase 5: Baseline ML Model (Chronological RF, Brier Score).
- [x] Phase 7: Historical Analogue Engine (k-NN similarity search).
- [x] Phase 10: Backend API (FastAPI endpoints for probabilities, regions, analogues).
- [x] Phase 11: Dashboard (Next.js Professional OCC theme, Risk Map, Intelligence Panel).
- [x] Phase 12: Full Integration (ML Engine connected to API).
- [x] Phase 13: Final Validation (Pipeline latency and output range verified).

## Current Architecture
- Backend: FastAPI (Python)
- ML: Scikit-learn (Random Forest) / Xarray (Data Handling)
- Frontend: Next.js 14 (TypeScript) + Tailwind CSS + Leaflet
- Data: GRIB/NetCDF $\to$ Xarray $\to$ Pandas $\to$ ML $\to$ API $\to$ Frontend

## Implemented Features
- Full ML pipeline for forecast bust detection in the Indian domain.
- Historical similarity search for evidence-based forecasting.
- Operational API providing real-time risk metrics.
- High-fidelity "Control Center" Dashboard.

## Dataset Information
- Targeted: Indian Domain (6N-38N, 68E-98E).
- Supports Lead-times Day 1 to Day 10.

## ML Model
- Baseline: RandomForestClassifier with chronological splitting to prevent leakage.
- Evaluation: Brier Score.

## Current API
- `/api/bust-probability`: Returns gridded probability map.
- `/api/risk-regions`: Returns GeoJSON high-risk clusters.
- `/api/analogues`: Returns historical analogues.
- `/api/explanations`: Returns contributing meteorological factors.

## Frontend Status
- UI implemented with "Operational Control Center" aesthetic.
- Real-time connectivity to the backend API logic.

## Decisions Made
- Zero fabrication of meteorological data.
- Strictly chronological validation.
- Operational Dark Theme with semantic risk colors.

## Next Tasks
- Deployment to production environment via Docker.
- Expansion to more meteorological variables.
