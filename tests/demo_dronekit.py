from dronekit import connect

# The connection string MUST include the protocol (udp:) for DroneKit to work
connection_string = 'udp:127.0.0.1:14550'

print(f"Attempting to connect to {connection_string}...")

try:
    # Connect to the Vehicle
    vehicle = connect(connection_string, wait_ready=True, heartbeat_timeout=30)
    
    print("Connected successfully!")
    print(f"Vehicle system ID: {vehicle.system_id}")
    print(f"Vehicle mode: {vehicle.mode.name}")
    
    # Close connection
    vehicle.close()
    print("Connection closed.")

except Exception as e:
    print(f"Connection failed: {e}")
