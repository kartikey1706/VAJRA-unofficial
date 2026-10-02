# Product Requirements Document (PRD) - VAJRA

## 1. Product Overview
**VAJRA** is an AI-powered Forecast Bust Detection system for medium-range weather forecasts. Unlike traditional Numerical Weather Prediction (NWP) models that provide a "best estimate" of weather, VAJRA estimates the **probability of a large forecast error (a "bust")**. It identifies where and when a forecast is likely to fail, providing meteorologists and decision-makers with a confidence metric to accompany the raw forecast.

## 2. Problem Statement
Medium-range forecasts (Day 1-10) often fail during complex atmospheric regimes (e.g., Monsoon depressions, Tropical Cyclones, Western Disturbances). These "busts" lead to operational failures. Currently, there is no systematic, AI-driven way to quantify the probability of a bust across a geographic region and lead time based on historical analogue performance and current ensemble disagreement.

## 3. Goals
- Estimate the probability of a "forecast bust" for specific grid cells and lead times.
- Provide a "Forecast Confidence" indicator (Low/Medium/High).
- Identify high-risk geographical clusters.
- Provide explainable signals (e.g., ensemble spread, historical analogues) for the bust probability.
- Build a production-ready prototype with real-world meteorological data.

## 4. Non-Goals
- VAJRA is **not** a weather forecast model. It does not predict the weather; it predicts the *error* of other models.
- It does not replace NWP models; it complements them.
- It does not provide absolute certainty of a bust.

## 5. Target Users
- **Meteorologists:** Need to know when to trust the model vs. when to rely on experience.
- **Weather Analysts:** Require regional risk maps for operational briefings.
- **Operational Decision Makers:** Need quick confidence levels for resource allocation.
- **Energy/Agriculture Teams:** Need reliability metrics for weather-dependent planning.

## 6. User Personas
- *Amit, Senior Forecaster:* Uses VAJRA to identify if the Day 5 rainfall forecast for Central India is likely to bust due to a poorly captured monsoon depression.
- *Priya, Risk Manager:* Needs to know if the "High Confidence" label for a heatwave forecast allows for triggering emergency protocols.

## 7. User Stories
- As a forecaster, I want to see a map of bust probabilities for Day 3 so I can manually adjust the forecast in high-risk areas.
- As an analyst, I want to know *why* a region is marked as "Low Confidence" (e.g., "High Ensemble Spread").
- As a decision-maker, I want to see a list of high-risk clusters for the next 7 days.

## 8. Functional Requirements
### 8.1 Core Outputs
- **Bust Probability Map:** A geospatial map displaying the probability (0-100%) of a large forecast error.
- **Confidence Maps:** Reliability views for each lead time (Day 1 to Day 10).
- **Risk Region Detection:** Automatic clustering of high-probability bust cells.
- **Explainable Assessment:** Textual/visual reasons for low confidence (e.g., "Historical analogue error: High").

### 8.2 Features
- **Lead-Time Selector:** Toggle between Day 1 and Day 10.
- **Variable Selector:** Select variables (Temp, Precip, Wind, etc.) to check reliability for.
- **Analogue Engine:** Search for historical atmospheric states similar to the current one and report their subsequent error rates.
- **Confidence Mapping:** Convert probability to labels (e.g., >70% $\to$ LOW).

## 9. Non-Functional Requirements
- **Data Integrity:** Zero fabrication of data. All values must be derived from real NWP/Observation datasets.
- **Performance:** API responses for probability maps must be under 2 seconds.
- **Scalability:** Architecture must support expanding the historical archive.
- **Interpretability:** ML models must provide feature importance or SHAP values.

## 10. Data Requirements
- **Real NWP Data:** Global/Regional medium-range models (GRIB/NetCDF).
- **Ensemble Data:** Multi-member ensemble forecasts (spread, mean).
- **Observations:** Real-world ground truth for verification (Station data/Reanalysis).
- **Historical Archive:** Multi-year records of forecasts and outcomes.

## 11. ML Requirements
- **Supervised Learning:** Regression/Classification to predict bust probability.
- **Chronological Validation:** No random splitting; use a time-series split to prevent data leakage.
- **Calibration:** Probabilities must be calibrated using Platt scaling or Isotonic regression.
- **Feature Set:** Ensemble spread, spatial gradients, regime indicators, analogue similarity.

## 12. Forecast Bust Definition
A "Bust" is defined as a forecast error exceeding a **configurable threshold** (e.g., $\text{Error} > X \cdot \sigma$ or $\text{MAE} > \text{Threshold}$). The threshold is variable based on the meteorological parameter.

## 13. Confidence Requirements
Confidence is a derived label based on the Bust Probability:
- **High Confidence:** Bust Prob < 30%
- **Medium Confidence:** 30% $\le$ Bust Prob < 70%
- **Low Confidence:** Bust Prob $\ge$ 70%
*(Thresholds are configurable)*.

## 14. Explainability Requirements
For every prediction, the system must provide:
1. Top 3 contributing features (e.g., Ensemble Spread).
2. Performance of the top 3 historical analogues.

## 15. Historical Analogue Requirements
- Feature-based similarity search (e.g., Euclidean distance or Cosine similarity in atmospheric state space).
- Retrieval of the actual error observed in those analogues.

## 16. Dashboard Requirements
- **Operational Dark Theme:** Professional meteorological aesthetic.
- **Interactive Map:** Using geospatial libraries (e.g., Leaflet/Mapbox) with color-coded risk layers.
- **Details Panel:** Clickable regions showing bust probability and reasons.

## 17. API Requirements
- RESTful API using FastAPI.
- Endpoints for `/bust-probability`, `/risk-regions`, `/analogues`.
- Versioned API (e.g., `/v1/`).

## 18. Error Handling
- Graceful handling of missing observation data.
- Clear "Data Unavailable" indicators on the map.
- Validation of input coordinate ranges.

## 19. Data Quality Requirements
- Automated checks for NaN values and coordinate shifts.
- Unit normalization (e.g., Kelvin to Celsius).

## 20. Security Considerations
- API Key authentication for internal access.
- Input sanitization to prevent injection.

## 21. Performance Requirements
- Use of Xarray and Zarr for efficient handling of large multidimensional arrays.
- Caching of frequent analogue searches.

## 22. MVP Scope
- Support for 1-2 primary variables (e.g., Temperature, Precipitation).
- Implementation of the end-to-end pipeline: Data $\to$ Bust Label $\to$ ML Model $\to$ API $\to$ Dashboard.
- Baseline ML model (e.g., Random Forest).
- Basic Historical Analogue search.
- Lead-time selector for Day 1-10.

## 23. Future Scope
- Expansion to more meteorological variables.
- Integration of deep learning (e.g., Graph Neural Networks for spatial patterns).
- Real-time data stream integration.
- User-defined bust thresholds.

## 24. Acceptance Criteria
- System can take a current forecast and output a probability map.
- Historical analogues are retrieved based on actual data similarity.
- The frontend displays real data from the backend API.
- No data leakage in the ML training process.

## 25. Success Metrics
- **Brier Score:** To measure the accuracy of probability predictions.
- **Reliability Diagram:** To check calibration of bust probabilities.
- **User Acceptance:** Meteorologists find the "Confidence" label helpful.
