import logging
import sys
from pathlib import Path
import yaml
from typing import Any, Dict

class VAJRALogger:
    """Global logging system for VAJRA."""
    _logger = None

    @classmethod
    def get_logger(cls, name: str = "VAJRA"):
        if cls._logger is None:
            # Load config for log level
            try:
                with open("config.yaml", "r") as f:
                    config = yaml.safe_load(f)
                    log_level = config.get("system", {}).get("log_level", "INFO")
            except Exception:
                log_level = "INFO"

            logging.basicConfig(
                level=getattr(logging, log_level.upper(), logging.INFO),
                format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                handlers=[
                    logging.StreamHandler(sys.stdout),
                    logging.FileHandler("vajra.log")
                ]
            )
            cls._logger = logging.getLogger(name)
        return cls._logger

def get_config() -> Dict[str, Any]:
    """Load system configuration."""
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

# Initialize global logger instance for easy access
logger = VAJRALogger.get_logger()
