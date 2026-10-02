from datetime import datetime
from typing import List, Tuple

import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel

from app.core.logger import logger
from app.data.nwp_loader import NWPDataLoader
from app.ml.analogues import AnalogueEngine
from app.ml.feature_engineering import FeatureEngineer
from app.ml.predictor import BustPredictor
from app.services.aligner import DataAligner


# ============================================================
# RESPONSE MODELS
# ============================================================

class ProbabilityPoint(BaseModel):
    lat: float
    lon: float
    probability: float
    confidence: str


class RiskRegion(BaseModel):
    region_id: str
    coords: List[List[float]]
    avg_probability: float
    confidence: str


class AnalogueCase(BaseModel):
    similarity: float
    outcome: str
    index: int


class Explanation(BaseModel):
    factor: str
    impact: str


# ============================================================
# VAJRA ENGINE
# ============================================================

class VAJRAEngine:
    """
    Main orchestration engine for the VAJRA ML pipeline.
    """

    def __init__(self):
        self.loader = NWPDataLoader()
        self.aligner = DataAligner()
        self.engineer = FeatureEngineer()
        self.predictor = BustPredictor()

        try:
            self.predictor.load_model()
            logger.info("ML model loaded successfully.")

        except Exception as e:
            logger.warning(
                f"No pre-trained model found, using fresh baseline: {e}"
            )

        self.historical_features = pd.DataFrame()
        self.historical_outcomes = pd.Series(dtype=float)
        self.analogue_engine = None

    def set_historical_data(
        self,
        features: pd.DataFrame,
        outcomes: pd.Series
    ):
        self.historical_features = features
        self.historical_outcomes = outcomes

        self.analogue_engine = AnalogueEngine(
            features,
            outcomes
        )

    def predict_bust(
        self,
        lead_time: int,
        variable: str,
        lat: float,
        lon: float
    ) -> Tuple[float, str]:

        # Temporary feature vector.
        # Replace with real NWP/observation features
        # when the complete data pipeline is connected.
        current_state = np.random.rand(10)

        try:
            probability = self.predictor.predict_probability(
                pd.DataFrame([current_state])
            )[0]

        except Exception as e:
            logger.warning(
                f"Prediction failed, using baseline probability: {e}"
            )
            probability = 0.5

        probability = float(
            np.clip(probability, 0.0, 1.0)
        )

        if probability < 0.3:
            confidence = "HIGH"
        elif probability < 0.7:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        return probability, confidence


# ============================================================
# ENGINE INITIALIZATION
# ============================================================

engine = VAJRAEngine()


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="VAJRA API",
    description="AI-Based Forecast Bust Detection System",
    version="0.1.0"
)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "VAJRA Backend",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================================================
# BUST PROBABILITY
# ============================================================

@app.get("/api/bust-probability")
async def get_bust_probability(
    lead_time: int = Query(..., ge=1, le=10),
    variable: str = Query("temperature")
):
    lats = np.linspace(6, 38, 20)
    lons = np.linspace(68, 98, 20)

    points = []

    for lat in lats:
        for lon in lons:

            probability, confidence = engine.predict_bust(
                lead_time=lead_time,
                variable=variable,
                lat=float(lat),
                lon=float(lon)
            )

            points.append(
                ProbabilityPoint(
                    lat=float(lat),
                    lon=float(lon),
                    probability=probability,
                    confidence=confidence
                )
            )

    return {
        "lead_time": lead_time,
        "variable": variable,
        "points": points
    }


# ============================================================
# RISK REGIONS
# ============================================================

@app.get("/api/risk-regions")
async def get_risk_regions(
    lead_time: int = Query(5, ge=1, le=10)
):
    regions = [
        RiskRegion(
            region_id="high_risk_cluster_1",
            coords=[
                [20.0, 75.0],
                [22.0, 75.0],
                [22.0, 78.0],
                [20.0, 78.0],
                [20.0, 75.0]
            ],
            avg_probability=0.82,
            confidence="LOW"
        )
    ]

    return {
        "lead_time": lead_time,
        "regions": regions
    }


# ============================================================
# ANALOGUE CASES
# ============================================================

@app.get("/api/analogues")
async def get_analogues(
    lat: float,
    lon: float
):

    if engine.analogue_engine is None:
        return {
            "analogues": [
                AnalogueCase(
                    similarity=0.90,
                    outcome="BUST",
                    index=1
                )
            ]
        }

    current_features = np.random.rand(10)

    try:
        analogues = engine.analogue_engine.find_similar_cases(
            current_features
        )

        return {
            "analogues": analogues
        }

    except Exception as e:
        logger.warning(
            f"Analogue search failed: {e}"
        )

        return {
            "analogues": []
        }


# ============================================================
# EXPLANATIONS
# ============================================================

@app.get("/api/explanations")
async def get_explanations(
    lat: float,
    lon: float
):

    explanations = [
        Explanation(
            factor="Ensemble Spread",
            impact="High"
        ),
        Explanation(
            factor="Regime: Monsoon Active",
            impact="Medium"
        ),
        Explanation(
            factor="Historical Analogue Error",
            impact="Low"
        )
    ]

    return {
        "latitude": lat,
        "longitude": lon,
        "explanations": explanations
    }


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
async def root():
    return {
        "project": "VAJRA",
        "message": "VAJRA Backend API is running",
        "docs": "/docs",
        "health": "/api/health"
    }


# ============================================================
# LOCAL DEVELOPMENT
# ============================================================

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )