from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DroneHealthEvent:
    drone_id: str
    battery_percentage: float | None
    gps_fix: int | None
    ekf_ok: bool
    armed: bool
    mode: str
    timestamp: datetime = datetime.now()
