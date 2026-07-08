from pymavlink import mavutil
import time

# Connect to the SITL instance
# Using the same endpoint that was failing in DroneKit
connection_string = "udp:127.0.0.1:14550"

print(f"Connecting to {connection_string}...")
master = mavutil.mavlink_connection(connection_string)

# Wait for a heartbeat
print("Waiting for heartbeat...")
msg = master.recv_match(type='HEARTBEAT', blocking=True, timeout=10)

if msg:
    print(f"Success! Received heartbeat: {msg}")
    print(f"System ID: {master.target_system}")
    print(f"Component ID: {master.target_component}")
else:
    print("Failed to receive heartbeat.")
