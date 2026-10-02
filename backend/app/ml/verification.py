import xarray as xr
import numpy as np
import yaml
from typing import Tuple, Dict, Any
from backend.app.core.logger import logger

class VerificationEngine:
    """
    Computes forecast errors and assigns 'Bust' labels based on
    meteorological thresholds.
    """
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.met_config = self.config['meteorology']

    def compute_error(self, forecast: xr.DataArray, observation: xr.DataArray) -> xr.DataArray:
        """
        Computes the absolute error between forecast and observation.
        Formula: Error = |Forecast - Observation|
        """
        try:
            # Ensure they are the same shape (should be handled by aligner)
            error = np.abs(forecast - observation)
            return error
        except Exception as e:
            logger.error(f"Error computation failed: {str(e)}")
            raise e

    def generate_bust_labels(self, error_map: xr.DataArray, variable_name: str) -> xr.DataArray:
        """
        Assigns a binary 'Bust' label (1 for bust, 0 for no-bust)
        based on the variable's threshold in config.yaml.
        """
        try:
            # Get threshold from config
            threshold = None
            for var in self.met_config['variables']:
                if var['name'] == variable_name:
                    threshold = var['bust_threshold']
                    break

            if threshold is None:
                raise ValueError(f"No bust threshold defined for variable: {variable_name}")

            # Generate binary mask: 1 if error > threshold, else 0
            bust_mask = (error_map > threshold).astype(int)
            logger.info(f"Generated bust labels for {variable_name} using threshold {threshold}")
            return bust_mask
        except Exception as e:
            logger.error(f"Bust labeling failed: {str(e)}")
            raise e

    def calculate_metrics(self, error_map: xr.DataArray) -> Dict[str, float]:
        """
        Computes global verification metrics for the dataset.
        """
        return {
            "MAE": float(error_map.mean()),
            "RMSE": float(np.sqrt((error_map**2).mean())),
            "MAX_ERROR": float(error_map.max())
        }
