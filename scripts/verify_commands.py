from swarm.drone.manager import SwarmManager
from loguru import logger
import time

class MockConfig:
    def __init__(self):
        self.mavlink = type('obj', (object,), {'endpoints': ["udpin:0.0.0.0:14550", "udpin:0.0.0.0:14560", "udpin:0.0.0.0:14570"]})
        self.connection = type('obj', (object,), {'wait_ready': False, 'heartbeat_timeout': 30})

manager = SwarmManager(MockConfig())
manager.connect_all()

print("--- Testing arm_all ---")
manager.arm_all()
time.sleep(2)

print("--- Testing mode_all ---")
manager.set_mode_all("GUIDED")
time.sleep(2)

print("--- Testing takeoff_all ---")
manager.takeoff_all(10.0)
time.sleep(2)

print("--- Verification Complete ---")
