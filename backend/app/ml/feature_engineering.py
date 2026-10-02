import xarray as xr
import numpy as np
from typing import Dict, Any
from app.core.logger import logger

class FeatureEngineer:
    """
    Transforms raw aligned NWP data into a feature set for the ML model.
    Focuses on indicators of forecast instability.
    """
    def __init__(self):
        self.logger = logger

    def compute_ensemble_features(self, ensemble_ds: xr.Dataset, variable: str) -> xr.Dataset:
        """
        Computes spread and variance from an ensemble forecast.
        Input ensemble_ds should have a 'member' dimension.
        """
        try:
            # Ensemble Mean
            mean = ensemble_ds[variable].mean(dim='member')

            # Ensemble Spread (Standard Deviation)
            spread = ensemble_ds[variable].std(dim='member')

            # Coefficient of Variation (Normalized Spread)
            cv = spread / (mean + 1e-6)

            features = xr.Dataset({
                f"{variable}_mean": mean,
                f"{variable}_spread": spread,
                f"{variable}_cv": cv
            })

            self.logger.info(f"Computed ensemble features for {variable}")
            return features
        except Exception as e:
            self.logger.error(f"Ensemble feature engineering failed: {str(e)}")
            raise e

    def compute_spatial_features(self, ds: xr.DataArray) -> xr.Dataset:
        """
        Computes spatial gradients to detect sharp fronts or instability.
        """
        try:
            # Gradient along latitude and longitude
            grad_lat = np.gradient(ds.values, axis=0)
            grad_lon = np.gradient(ds.values, axis=1)

            # Total Magnitude of Gradient
            grad_mag = np.sqrt(grad_lat**2 + grad_lon**2)

            features = xr.Dataset({
                "spatial_gradient_mag": (("lat", "lon"), grad_mag)
            })
            # Copy coordinates
            features.coords['lat'] = ds.lat
            features.coords['lon'] = ds.lon

            return features
        except Exception as e:
            self.logger.error(f"Spatial feature engineering failed: {str(e)}")
            raise e

    def detect_regimes(self, ds: xr.Dataset) -> xr.DataArray:
        """
        Simple rule-based or clustering regime detection.
        Example: Identify 'Active Monsoon' based on precipitation and pressure.
        """
        # Prototype: Simple threshold-based regime
        # In a real scenario, this would be a K-Means cluster of the pressure field
        try:
            # Assume we have precipitation and pressure
            precip = ds['precipitation']
            pressure = ds['pressure']

            # Regime 1: Active Monsoon (High Precip, Low Pressure)
            regime = xr.where((precip > 10) & (pressure < 1005), 1, 0)

            self.logger.info("Regime detection completed.")
            return regime
        except Exception as e:
            self.logger.error(f"Regime detection failed: {str(e)}")
            return xr.full_like(ds['precipitation'], 0)

    def build_feature_matrix(self, ensemble_ds: xr.Dataset, variable: str) -> xr.Dataset:
        """
        Orchestrates all feature extraction into a single dataset.
        """
        ensemble_feats = self.compute_ensemble_features(ensemble_ds, variable)
        spatial_feats = self.compute_spatial_features(ensemble_ds[variable].mean(dim='member'))
        regime_feats = self.detect_regimes(ensemble_ds)

        combined = xr.merge([ensemble_feats, spatial_feats])
        combined['regime_id'] = regime_feats

        return combined
