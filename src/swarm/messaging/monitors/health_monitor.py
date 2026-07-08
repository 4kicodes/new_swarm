from loguru import logger
from swarm.messaging.events import DroneHealthEvent

class HealthMonitor:
    def __init__(self, bus):
        self.bus = bus
        self.bus.subscribe("events/drone/health", self.handle_health_event)

    def handle_health_event(self, event: DroneHealthEvent):
        if not event.ekf_ok or event.battery_percentage < 20:
            logger.warning(f"CRITICAL HEALTH ALERT for {event.drone_id}: {event}")
        else:
            logger.info(f"Health update for {event.drone_id}: OK")
