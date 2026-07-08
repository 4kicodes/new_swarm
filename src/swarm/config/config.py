"""
Configuration loader for the Drone Swarm Framework.
"""

from pathlib import Path
from typing import Union
import yaml

def load_config(path: Union[str, Path, None] = None) -> dict:
    """Load and return the framework configuration."""
    if path is None:
        path = Path(__file__).resolve().parent.parent / "config.yaml"
    
    with Path(path).open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)
