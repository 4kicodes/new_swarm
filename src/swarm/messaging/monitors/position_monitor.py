import threading
from typing import Dict, Optional
from swarm.messaging.topics import TOPIC_DRONE_POSITION, TOPIC_DRONE_CONNECTION
from swarm.messaging.events import DronePositionEvent, ConnectionEvent
from loguru import logger

class PositionMonitor:
    def __init__(self, bus):
        self.bus = bus
        self._positions: Dict[str, DronePositionEvent] = {}
        self._lock = threading.RLock()
        
        # Subscribe to topics
        self.bus.subscribe(TOPIC_DRONE_POSITION, self._handle_position_event)
        self.bus.subscribe(TOPIC_DRONE_CONNECTION, self._handle_connection_event)
        logger.info("PositionMonitor initialized and subscribed to topics.")

    def _handle_position_event(self, event: DronePositionEvent):
        with self._lock:
            self._positions[event.drone_id] = event
            logger.debug(f"Position updated for {event.drone_id}")

    def _handle_connection_event(self, event: ConnectionEvent):
        if event.status == "disconnected":
            with self._lock:
                if event.drone_id in self._positions:
                    del self._positions[event.drone_id]
                    logger.info(f"Position cleaned up for disconnected drone: {event.drone_id}")

    def get_position(self, drone_id: str) -> Optional[DronePositionEvent]:
        with self._lock:
            return self._positions.get(drone_id)

    def get_all_positions(self) -> Dict[str, DronePositionEvent]:
        with self._lock:
            return dict(self._positions)
