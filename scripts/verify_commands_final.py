from swarm.drone.manager import SwarmManager
from loguru import logger
import time

class MockConfig:
    def __init__(self):
        self.mavlink = type('obj', (object,), {'endpoints': ["udpin:0.0.0.0:14550", "udpin:0.0.0.0:14560", "udpin:0.0.0.0:14570"]})
        self.connection = type('obj', (object,), {'wait_ready': False, 'heartbeat_timeout': 30})

manager = SwarmManager(MockConfig())
manager.connect_all()

# Helper to print drone state
def print_swarm_state(label):
    print(f"\n--- State Verification: {label} ---")
    for drone_id, conn in manager.connections.items():
        vehicle = conn.vehicle
        print(f"Drone {drone_id}: Armed={vehicle.armed}, Mode={vehicle.mode.name}, Altitude={vehicle.location.global_relative_frame.alt}")

# 1. Verify Initial State
print_swarm_state("Initial")

# 2. Test Arming
print("\n--- Sending 'arm all' ---")
manager.arm_all()
time.sleep(3)
print_swarm_state("Post-Arm")

# 3. Test Mode Change
print("\n--- Sending 'mode all GUIDED' ---")
manager.set_mode_all("GUIDED")
time.sleep(3)
print_swarm_state("Post-Mode")

# 4. Test Takeoff
print("\n--- Sending 'takeoff all 10m' ---")
manager.takeoff_all(10.0)
time.sleep(5) 
print_swarm_state("Post-Takeoff")

# 5. Test Land
print("\n--- Sending 'land all' ---")
manager.land_all()
time.sleep(5)
print_swarm_state("Post-Land")

print("\n--- Verification Complete ---")
