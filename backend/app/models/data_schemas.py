from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class DatasetMetadata(BaseModel):
    """Metadata for an ingested meteorological dataset."""
    dataset_id: str
    source: str  # e.g., "GFS", "ECMWF", "ERA5"
    variable_name: str
    unit: str
    spatial_resolution: float
    forecast_cycle: datetime
    lead_times: List[int]
    dimensions: Dict[str, int]  # e.g., {"lat": 720, "lon": 1440}

class IngestionLog(BaseModel):
    """Log for tracking data ingestion events."""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    dataset_id: str
    status: str  # "SUCCESS", "FAILED"
    files_processed: int
    error_message: Optional[str] = None
