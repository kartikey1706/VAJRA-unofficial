import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import brier_score_loss, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path
from typing import Tuple, Dict, Any
from app.core.logger import logger

class BustPredictor:
    """
    Baseline ML model to predict the probability of a forecast bust.
    Uses chronological validation to prevent data leakage.
    """
    def __init__(self, model_path: str = "models/bust_model_v1.joblib"):
        self.model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        self.scaler = StandardScaler()
        self.model_path = Path(model_path)

    def prepare_data(self, features_ds: Any, labels_ds: Any) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Converts xarray datasets to pandas DataFrames for Scikit-learn.
        """
        # Flatten spatial and temporal dimensions into rows
        df_feats = features_ds.to_dataframe().dropna()
        df_labels = labels_ds.to_dataframe().dropna()

        # Align indices
        common_idx = df_feats.index.intersection(df_labels.index)
        X = df_feats.loc[common_idx]
        y = df_labels.loc[common_idx].iloc[:, 0]

        return X, y

    def train_chronological(self, X: pd.DataFrame, y: pd.Series, split_ratio: float = 0.8):
        """
        Splits data chronologically (no shuffling) to avoid future leakage.
        """
        split_idx = int(len(X) * split_ratio)

        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.model.fit(X_train_scaled, y_train)

        # Evaluate
        probs = self.model.predict_proba(X_test_scaled)[:, 1]
        preds = self.model.predict(X_test_scaled)

        metrics = {
            "brier_score": brier_score_loss(y_test, probs),
            "accuracy": accuracy_score(y_test, preds),
            "report": classification_report(y_test, preds)
        }

        logger.info(f"Model trained. Brier Score: {metrics['brier_score']:.4f}")
        return metrics

    def save_model(self):
        """Persists the model and scaler to disk."""
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({"model": self.model, "scaler": self.scaler}, self.model_path)
        logger.info(f"Model saved to {self.model_path}")

    def load_model(self):
        """Loads the model and scaler from disk."""
        data = joblib.load(self.model_path)
        self.model = data["model"]
        self.scaler = data["scaler"]
        logger.info(f"Model loaded from {self.model_path}")

    def predict_probability(self, X: pd.DataFrame) -> np.ndarray:
        """Predicts the probability of a bust for given features."""
        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)[:, 1]
