import xarray as xr
import numpy as np
import yaml
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from app.core.logger import logger
from app.models.data_schemas import DatasetMetadata

class NWPDataLoader:
    """
    Handles ingestion of Numerical Weather Prediction (NWP) data in GRIB or NetCDF formats.
    Designed to be model-agnostic.
    """
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.raw_data_path = Path(self.config['paths']['data_raw'])
        self.logger = logger

    def load_grib(self, file_path: str, filter_by_keys: Optional[Dict[str, Any]] = None) -> xr.Dataset:
        """Loads a GRIB file into an xarray Dataset."""
        try:
            self.logger.info(f"Loading GRIB file: {file_path}")
            # Using engine='cfgrib' for GRIB files
            ds = xr.open_dataset(file_path, engine='cfgrib', filter_by_keys=filter_by_keys)
            return ds
        except Exception as e:
            self.logger.error(f"Failed to load GRIB file {file_path}: {str(e)}")
            raise e

    def load_netcdf(self, file_path: str) -> xr.Dataset:
        """Loads a NetCDF file into an xarray Dataset."""
        try:
            self.logger.info(f"Loading NetCDF file: {file_path}")
            ds = xr.open_dataset(file_path, engine='netcdf4')
            return ds
        except Exception as e:
            self.logger.error(f"Failed to load NetCDF file {file_path}: {str(e)}")
            raise e

    def extract_indian_domain(self, ds: xr.Dataset) -> xr.Dataset:
        """Slices the dataset to the Indian domain specified in config.yaml."""
        lat_range = self.config['meteorology']['lat_range']
        lon_range = self.config['meteorology']['lon_range']

        # Handle different naming conventions for lat/lon (e.g., 'latitude' vs 'lat')
        lat_name = 'latitude' if 'latitude' in ds.coords else 'lat'
        lon_name = 'longitude' if 'longitude' in ds.coords else 'lon'

        try:
            # Slicing to the Indian domain
            ds_indian = ds.sel({
                lat_name: slice(lat_range[1], lat_range[0]), # GRIB often uses North to South
                lon_name: slice(lon_range[0], lon_range[1])
            })
            self.logger.info(f"Extracted Indian domain: {lat_range}N, {lon_range}E")
            return ds_indian
        except Exception as e:
            self.logger.error(f"Error slicing to Indian domain: {str(e)}")
            raise e

    def validate_dataset(self, ds: xr.Dataset) -> bool:
        """Performs basic data quality checks on the ingested dataset."""
        if ds.dims == {}:
            self.logger.warning("Dataset has no dimensions.")
            return False

        # Check for excessive NaNs (e.g., > 50%)
        for var in ds.data_vars:
            nan_fraction = np.isnan(ds[var].values).mean()
            if nan_fraction > 0.5:
                self.logger.warning(f"Variable {var} contains {nan_fraction:.2%} NaNs.")
                return False

        return True

    def get_metadata(self, ds: xr.Dataset, source: str, variable: str) -> DatasetMetadata:
        """Extracts metadata from the loaded xarray dataset."""
        # Simplified metadata extraction
        return DatasetMetadata(
            dataset_id=f"{source}_{variable}",
            source=source,
            variable_name=variable,
            unit=str(ds[variable].attrs.get('units', 'unknown')),
            spatial_resolution=float(ds.attrs.get('grid_resolution', 0.0)),
            forecast_cycle=datetime.now(), # Simplified for prototype
            lead_times=list(range(1, 11)),
            dimensions={dim: ds.dims[dim] for dim in ds.dims}
        )
