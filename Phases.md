# Implementation Phases - VAJRA

## Phase 0: Project Foundation
**Objective:** Setup the development environment and project structure.
- [ ] Initialize Git repository and folder structure.
- [ ] Configure Python environment (poetry/conda) and Node.js environment.
- [ ] Implement global logging and configuration system (`config.yaml`).
- [ ] Setup `.env` for paths and secrets.
- **Acceptance Criteria:** Project boots without errors; logging is functional.

## Phase 1: Data Ingestion
**Objective:** Load real NWP and observation data into the system.
- [ ] Define schemas for Forecast and Observation data.
- [ ] Build GRIB/NetCDF loaders using `xarray`.
- [ ] Ingest sample real-world Indian domain datasets (NWP + ERA5/Station).
- [ ] Implement basic data validation (NaN checks, coordinate verification).
- **Inputs:** GRIB/NetCDF files.
- **Outputs:** Xarray datasets.
- **Acceptance Criteria:** Data is loaded into memory/disk with correct dimensions and units.

## Phase 2: Data Alignment
**Objective:** Standardize spatial and temporal grids.
- [ ] Implement bilinear interpolation for spatial alignment.
- [ ] Align forecast cycles with valid times.
- [ ] Standardize lead-times (Day 1 to Day 10).
- [ ] Normalize units.
- **Acceptance Criteria:** Forecasts and observations exist on the same grid and time axis.

## Phase 3: Forecast Verification & Bust Labeling
**Objective:** Quantify model error and define "Busts".
- [ ] Compute point-wise errors (MAE, RMSE) for selected variables.
- [ ] Implement the **Configurable Bust Threshold** logic.
- [ ] Generate binary `is_bust` labels for the historical archive.
- **Outputs:** Labeled dataset (Feature $\to$ Bust).
- **Acceptance Criteria:** Labels correctly identify historically failed forecasts.

## Phase 4: Feature Engineering
**Objective:** Create ML-ready predictors.
- [ ] Compute ensemble spread and standard deviation.
- [ ] Derive atmospheric diagnostics (gradients, vorticity).
- [ ] Implement Regime Detection (Clustering on pressure/temp fields).
- [ ] Extract lead-time features.
- **Acceptance Criteria:** A feature matrix exists where each row is a (time, space, lead_time) tuple.

## Phase 5: Baseline ML Model
**Objective:** Establish a predictive baseline.
- [ ] Train a baseline classifier (e.g., Random Forest) to predict `is_bust`.
- [ ] Evaluate using a chronological split (Time-Series Validation).
- [ ] Generate raw bust probabilities.
- **Acceptance Criteria:** Model outperforms a random guess; Brier Score is calculated.

## Phase 6: Regime-Aware Prediction
**Objective:** Incorporate atmospheric regimes into the model.
- [ ] Integrate regime IDs as model features.
- [ ] Evaluate performance gain per regime (e.g., "Monsoon Active" vs "Break").
- **Acceptance Criteria:** Regime-specific error analysis is performed.

## Phase 7: Historical Analogue Engine
**Objective:** Find similar past cases to support predictions.
- [ ] Implement feature-based similarity search (k-NN).
- [ ] Retrieve actual outcomes of the top $K$ analogues.
- [ ] Calculate "Analogue Error Rate".
- **Acceptance Criteria:** System can retrieve 3-5 similar cases from 10 years of data.

## Phase 8: Probability Calibration
**Objective:** Ensure probabilities are operationally meaningful.
- [ ] Generate reliability diagrams.
- [ ] Apply Isotonic Regression/Platt Scaling.
- [ ] Validate calibrated probabilities against a hold-out set.
- **Acceptance Criteria:** Calibration curve is close to the 45-degree line.

## Phase 9: Explainability
**Objective:** Make the "Black Box" transparent.
- [ ] Implement SHAP for local grid-cell explanations.
- [ ] Link analogue cases to the "Why" panel.
- **Acceptance Criteria:** User can see the top 3 reasons for a "Low Confidence" rating.

## Phase 10: Backend API
**Objective:** Expose ML results via REST.
- [ ] Build FastAPI endpoints for probability maps and risk regions.
- [ ] Implement GeoJSON exporters for risk clusters.
- [ ] Integrate the ML inference pipeline into the API.
- **Acceptance Criteria:** API returns valid JSON/GeoJSON in < 2s.

## Phase 11: Dashboard
**Objective:** Visualize the results operationally.
- [ ] Build the Dark-Theme UI.
- [ ] Integrate interactive map with bust-probability layers.
- [ ] Implement Lead-Time and Variable selectors.
- [ ] Build the Region Details and Explanation panels.
- **Acceptance Criteria:** Frontend reflects real-time data from the API.

## Phase 12: Integration & Testing
**Objective:** End-to-end validation.
- [ ] Full pipeline run: Raw Data $\to$ Dashboard.
- [ ] Unit tests for data loaders and ML logic.
- [ ] Integration tests for API $\to$ Frontend.
- **Acceptance Criteria:** System is stable; no data leakage detected.

## Phase 13: Deployment
**Objective:** Setup production-ready environment.
- [ ] Create Docker Compose for all services.
- [ ] Setup environment variable management.
- [ ] Write deployment documentation.
- **Acceptance Criteria:** System is deployable on a single command.
