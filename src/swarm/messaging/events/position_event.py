from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DronePositionEvent:
    drone_id: str
    latitude: float
    longitude: float
    altitude_msl: float
    relative_altitude: float
    heading: float
    ground_speed: float
    # Velocity fields
    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0
    timestamp: datetime = datetime.now()
