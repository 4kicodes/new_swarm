from dataclasses import dataclass
from datetime import datetime

@dataclass
class ConnectionEvent:
    drone_id: str
    status: str  # "connected", "disconnected"
    timestamp: datetime = datetime.now()
