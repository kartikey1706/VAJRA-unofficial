import xarray as xr
import numpy as np
from typing import Tuple, List, Dict, Any
from app.core.logger import logger
import yaml

class DataAligner:
    """
    Handles the critical task of ensuring that forecasts and observations
    share the same spatial grid and temporal axis.
    """
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.lat_range = self.config['meteorology']['lat_range']
        self.lon_range = self.config['meteorology']['lon_range']

    def standardize_grid(self, ds: xr.Dataset, target_res: float = 1.0) -> xr.Dataset:
        """
        Regrids a dataset to a standard resolution using bilinear interpolation.
        Example: Regrid 0.25° GFS to 1.0° for consistency across models.
        """
        try:
            # Create new coordinate arrays based on target resolution
            new_lat = np.linspace(self.lat_range[0], self.lat_range[1],
                                  int((self.lat_range[1] - self.lat_range[0]) / target_res))
            new_lon = np.linspace(self.lon_range[0], self.lon_range[1],
                                  int((self.lon_range[1] - self.lon_range[0]) / target_res))

            # Identify lat/lon names
            lat_name = 'latitude' if 'latitude' in ds.coords else 'lat'
            lon_name = 'longitude' if 'longitude' in ds.coords else 'lon'

            # Interpolate to the new grid
            ds_regridded = ds.interp(
                {lat_name: new_lat, lon_name: new_lon},
                method="linear"
            )
            logger.info(f"Regridded dataset to {target_res}° resolution.")
            return ds_regridded
        except Exception as e:
            logger.error(f"Regridding failed: {str(e)}")
            raise e

    def align_time_axis(self, forecast_ds: xr.Dataset, obs_ds: xr.Dataset) -> Tuple[xr.Dataset, xr.Dataset]:
        """
        Aligns the time dimensions of forecasts and observations.
        Ensures that Forecast Valid Time == Observation Time.
        """
        try:
            # Find common time steps
            common_times = np.intersect1d(forecast_ds.time.values, obs_ds.time.values)
            if len(common_times) == 0:
                raise ValueError("No overlapping time steps found between forecast and observations.")

            f_aligned = forecast_ds.sel(time=common_times)
            o_aligned = obs_ds.sel(time=common_times)

            logger.info(f"Aligned time axis. Common time steps: {len(common_times)}")
            return f_aligned, o_aligned
        except Exception as e:
            logger.error(f"Temporal alignment failed: {str(e)}")
            raise e

    def normalize_units(self, ds: xr.Dataset, variable: str, target_unit: str) -> xr.Dataset:
        """
        Ensures consistency in units (e.g., converting Kelvin to Celsius).
        """
        # Implementation for common conversions
        if variable == "temperature" and target_unit == "C":
            # Assume input is Kelvin
            ds[variable] = ds[variable] - 273.15
            ds[variable].attrs['units'] = 'C'

        return ds
