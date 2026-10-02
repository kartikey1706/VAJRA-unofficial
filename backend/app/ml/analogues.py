import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from typing import List, Dict, Any, Tuple
from app.core.logger import logger
class AnalogueEngine:
    """
    Retrieves historically similar forecast situations to provide
    evidence for the bust probability.
    """
    def __init__(self, historical_features: pd.DataFrame, historical_outcomes: pd.Series):
        """
        Args:
            historical_features: DataFrame of features for all past cases.
            historical_outcomes: Series of binary bust labels for those cases.
        """
        self.features = historical_features
        self.outcomes = historical_outcomes
        # Use BallTree or KDTree for efficient spatial search
        self.nn = NearestNeighbors(n_neighbors=5, metric='euclidean')
        self.nn.fit(historical_features)
        self.logger = logger

    def find_similar_cases(self, current_features: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        """
        Finds the K most similar historical cases.
        """
        try:
            distances, indices = self.nn.kneighbors(current_features.reshape(1, -1), n_neighbors=k)

            analogues = []
            for dist, idx in zip(distances[0], indices[0]):
                outcome = self.outcomes.iloc[idx]
                analogues.append({
                    "similarity": 1 / (1 + dist), # Convert distance to similarity score
                    "outcome": "BUST" if outcome == 1 else "NO_BUST",
                    "index": idx
                })

            self.logger.info(f"Retrieved {k} analogues for current state.")
            return analogues
        except Exception as e:
            self.logger.error(f"Analogue search failed: {str(e)}")
            return []

    def get_analogue_error_rate(self, current_features: np.ndarray, k: int = 5) -> float:
        """
        Calculates the percentage of retrieved analogues that resulted in a bust.
        """
        cases = self.find_similar_cases(current_features, k=k)
        if not cases:
            return 0.0

        bust_count = sum(1 for c in cases if c['outcome'] == "BUST")
        return bust_count / len(cases)
