# Architecture Document - VAJRA

## 1. System Architecture Overview
VAJRA is designed as a modular, data-driven pipeline that transforms raw Numerical Weather Prediction (NWP) data into actionable forecast-confidence metrics.

### High-Level Data Flow
`Data Sources` $\to$ `Ingestion` $\to$ `Preprocessing/Alignment` $\to$ `Bust Labeling` $\to$ `Feature Engineering` $\to$ `ML/Analogue Engine` $\to$ `Calibration` $\to$ `API` $\to$ `Dashboard`

## 2. Component Architecture

### 2.1 Data Layer
- **Sources:** GRIB/NetCDF files from Global (e.g., GFS, ECMWF) and Regional models, and Observation data (ERA5, Station data).
- **Ingestion Service:** Python-based loaders using `xarray` and `cfgrib` to handle multidimensional weather data.
- **Storage:** 
    - **Large Datasets:** Zarr or NetCDF files stored in object storage (S3/Local).
    - **Metadata/Results:** PostgreSQL with PostGIS for spatial querying of risk regions.
    - **Model Artifacts:** MLflow or simple versioned `.pkl`/`.joblib` files.

### 2.2 Processing Pipeline
- **Alignment Engine:** Standardizes disparate grids (e.g., 0.25° to 1.0°) using bilinear interpolation. Aligns forecast cycles and valid times.
- **Verification Module:** Computes errors (MAE, RMSE) between historical forecasts and observations. Applies the **Configurable Bust Threshold** to generate binary labels (Bust vs. No-Bust).
- **Feature Factory:**
    - **Ensemble Features:** Calculates spread, standard deviation, and member-to-mean deviations.
    - **Atmospheric Diagnostics:** Computes vorticity, divergence, and spatial gradients.
    - **Regime Detector:** Clustering (K-Means) or rule-based identification of weather regimes (e.g., "Active Monsoon").

### 2.3 ML & Analogue Engine
- **Bust Prediction Model:** A supervised ML model (Baseline: Random Forest / XGBoost) trained to predict the probability of a bust given the current atmospheric state and ensemble spread.
- **Historical Analogue Engine:** 
    - **Encoding:** Current state represented as a feature vector.
    - **Search:** k-Nearest Neighbors (k-NN) search across the historical archive.
    - **Outcome Analysis:** Aggregates the error rates of retrieved neighbours.
- **Calibration Layer:** Applies Isotonic Regression to ensure the predicted 70% probability corresponds to a 70% historical bust rate.

### 2.4 Backend API
- **Framework:** FastAPI.
- **Pattern:** Service-Repository pattern.
- **Endpoints:**
    - `/bust-probability`: Returns a gridded probability map for a given lead time.
    - `/risk-regions`: Returns GeoJSON polygons of high-risk clusters.
    - `/analogues`: Returns details of the top $K$ historical similar cases.
    - `/explanations`: Returns SHAP values for a specific grid cell.

### 2.5 Frontend Dashboard
- **Framework:** Next.js + TypeScript.
- **Styling:** Tailwind CSS (Operational Dark Theme).
- **Visualization:** 
    - **Map:** Leaflet or Mapbox with custom Canvas/SVG layers for probability heatmaps.
    - **Analytics:** Recharts/Chart.js for lead-time confidence trends.

## 3. ML Pipeline Detail
1. **Split:** Chronological split (e.g., 2015-2020 Train, 2021 Val, 2022 Test).
2. **Training:** Target = `is_bust` (Binary). Features = `[Ensemble_Spread, Regime_ID, Lead_Time, Analogue_Error, ...]`.
3. **Inference:** `Input Forecast` $\to$ `Feature Extraction` $\to$ `Model Prediction` $\to$ `Probability Calibration` $\to$ `Output`.

## 4. Configuration & DevOps
- **Config Management:** `.env` for secrets and `config.yaml` for meteorological thresholds.
- **Logging:** Structured logging using `loguru`.
- **Deployment:** 
    - **Containerization:** Docker Compose for Backend, Frontend, and PostgreSQL.
    - **CI/CD:** GitHub Actions for linting and testing.

## 5. Error Handling & Monitoring
- **Data Gaps:** Linear interpolation for small gaps; "Data Unavailable" flags for large gaps.
- **Model Drift:** Periodic monitoring of the Brier Score on new data.
- **API Health:** `/health` endpoint monitoring DB and Model connectivity.
