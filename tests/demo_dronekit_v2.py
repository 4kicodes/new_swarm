from dronekit import connect

# The docs state: connect('127.0.0.1:14550', ...)
# Let's try strictly as documented, though DroneKit usually *requires* a protocol.
connection_string = '127.0.0.1:14550'

print(f"Attempting to connect using documented syntax: {connection_string}...")

try:
    # Testing both wait_ready=True (as requested) and wait_ready=False to isolate the init failure
    vehicle = connect(connection_string, wait_ready=True, heartbeat_timeout=30)
    
    print("Connected successfully!")
    vehicle.close()
except Exception as e:
    print(f"Connection failed (wait_ready=True): {e}")

try:
    print("\nAttempting with wait_ready=False...")
    vehicle = connect(connection_string, wait_ready=False, heartbeat_timeout=30)
    print("Connected successfully (wait_ready=False)!")
    print(f"Vehicle mode: {vehicle.mode.name}")
    vehicle.close()
except Exception as e:
    print(f"Connection failed (wait_ready=False): {e}")
