from swarm.drone.manager import SwarmManager
from swarm.messaging.bus import InMemoryBus
from swarm.messaging.events import ConnectionEvent
from swarm.messaging.topics import TOPIC_DRONE_CONNECTION
from loguru import logger
import time

class MockConfig:
    def __init__(self):
        self.mavlink = type('obj', (object,), {'endpoints': ["udpin:0.0.0.0:14550"]})
        self.connection = type('obj', (object,), {'wait_ready': False, 'heartbeat_timeout': 30})

bus = InMemoryBus()
manager = SwarmManager(MockConfig(), bus)

received_events = []
def event_callback(event: ConnectionEvent):
    logger.info(f"Received event: {event}")
    received_events.append(event)

bus.subscribe(TOPIC_DRONE_CONNECTION, event_callback)

manager.connect_all()
time.sleep(2)
manager.disconnect_all()
time.sleep(1)

print(f"Total events received: {len(received_events)}")
for e in received_events:
    print(f" - {e}")
