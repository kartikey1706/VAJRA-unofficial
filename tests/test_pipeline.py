import numpy as np
import pandas as pd
from backend.app.ml.predictor import BustPredictor
from backend.app.ml.feature_engineering import FeatureEngineer
from backend.app.ml.verification import VerificationEngine
from backend.app.core.logger import logger

def run_full_validation_test():
    """
    End-to-end test of the VAJRA pipeline.
    """
    logger.info("Starting End-to-End Validation Test...")

    # 1. Simulate Data Ingestion & Alignment
    # Create mock features (1000 samples, 10 features)
    X = pd.DataFrame(np.random.rand(1000, 10), columns=[f"feat_{i}" for i in range(10)])
    # Create mock labels (Binary: Bust vs No-Bust)
    y = pd.Series(np.random.randint(0, 2, 1000))

    # 2. Test ML Predictor
    predictor = BustPredictor()
    metrics = predictor.train_chronological(X, y)

    logger.info(f"Validation Metrics: {metrics}")

    # 3. Test Inference Latency
    import time
    start = time.time()
    probs = predictor.predict_probability(X.iloc[-10:])
    end = time.time()

    logger.info(f"Inference latency for 10 points: {(end-start)*1000:.2f}ms")

    # 4. Verify output range
    assert np.all(probs >= 0) and np.all(probs <= 1), "Probabilities must be in [0, 1]"

    logger.info("End-to-End Validation Successful.")

if __name__ == "__main__":
    run_full_validation_test()
