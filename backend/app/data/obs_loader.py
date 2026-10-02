import xarray as xr
import numpy as np
from pathlib import Path
from backend.app.core.logger import logger

class ObservationLoader:
    """
    Handles ingestion of ground-truth observation data (e.g., ERA5 reanalysis or station data).
    """
    def __init__(self, config_path: str = "config.yaml"):
        import yaml
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.obs_path = Path(self.config['paths']['data_raw'])

    def load_observations(self, file_path: str) -> xr.Dataset:
        """Loads observation data (typically NetCDF)."""
        try:
            logger.info(f"Loading observation data: {file_path}")
            ds = xr.open_dataset(file_path, engine='netcdf4')
            return ds
        except Exception as e:
            logger.error(f"Failed to load observations {file_path}: {str(e)}")
            raise e

    def align_to_grid(self, obs_ds: xr.Dataset, target_ds: xr.Dataset) -> xr.Dataset:
        """
        Interpolates observation data to match the grid of the NWP forecast.
        Crucial for point-by-point verification.
        """
        try:
            # Interp uses linear interpolation by default
            aligned_obs = obs_ds.interp_like(target_ds)
            logger.info("Observations successfully aligned to NWP grid.")
            return aligned_obs
        except Exception as e:
            logger.error(f"Alignment failure: {str(e)}")
            raise e
