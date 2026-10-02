# Rules - VAJRA

## 1. General Coding Rules
- **Clean & Modular:** Write small, single-responsibility functions.
- **Type Safety:** Use Python type hints (`typing`) and TypeScript interfaces strictly.
- **Explicit Error Handling:** Use `try-except` blocks. Never use `pass` in an except block. Log errors with context.
- **Environment over Hardcoding:** All secrets, API keys, and file paths must be in `.env` or `config.yaml`.
- **Validation:** Validate all API inputs using Pydantic.

## 2. AI/ML Rules (Strict)
- **Zero Fabrication:** 
    - NEVER fabricate weather data.
    - NEVER fabricate observations.
    - NEVER fabricate forecast probabilities.
    - NEVER fabricate historical analogue cases.
- **Calibration:** Do not claim "calibrated probability" unless it has been validated against a reliability diagram.
- **No Absolute Certainty:** Never represent a bust probability as 100% or 0% certainty. Use terminology like "High Probability".
- **Temporal Integrity (No Leakage):**
    - Use strictly chronological validation.
    - Ensure features for a forecast at time $T$ only use data available at time $T$.
    - No random shuffling of time-series data.
- **Documentation:** Every feature used in the model must be documented (source, unit, physical meaning).
- **Versioning:** Track ML model versions (e.g., `v1_rf_precip_20231001.joblib`).

## 3. Meteorological Rules
- **Temporal Respect:** strictly adhere to `Forecast Cycle` and `Valid Time`.
- **Spatial Integrity:** Preserve coordinates. Do not change the grid resolution without documenting the interpolation method.
- **Units:** Preserve units (e.g., K, Pa, m/s). Document all transformations (e.g., Kelvin $\to$ Celsius).
- **Data Gaps:** Handle missing data explicitly. Do not fill gaps with means unless documented and justified.
- **Causality:** Do not infer physical causality from ML feature importance alone. Use them as "indicators".

## 4. Frontend Rules
- **No Fake Data:** Never display mock data as real. 
- **Demo Mode:** If using mock data for UI development, the dashboard MUST have a prominent "DEMO MODE" banner.
- **Contextual Metadata:** Always display:
    - Data Timestamp
    - Forecast Cycle
    - Lead Time (Day 1-10)
    - Data Quality Status
- **Semantic Colors:** 
    - Red = High Risk / Low Confidence
    - Yellow = Medium Risk
    - Green = High Confidence
    - Use these colors for meaning, not decoration.

## 5. API Rules
- **REST Standards:** Use appropriate HTTP verbs (GET, POST).
- **Status Codes:** Return `400` for bad requests, `404` for missing data, `500` for server errors.
- **Structured Responses:** All responses must be JSON.
- **Versioned Endpoints:** Use `/v1/` prefix for all public endpoints.
