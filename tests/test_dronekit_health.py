from dronekit import connect
import time

def test_drone_connection():
    connection_string = '127.0.0.1:14550'
    print(f"Connecting to {connection_string} (wait_ready=False)...")
    
    # 1. Connect without auto-wait
    vehicle = connect(connection_string, wait_ready=False, heartbeat_timeout=30)
    
    # 2. Manual initialization / Wait loop
    print("Waiting for essential vehicle data...")
    # Wait for the vehicle to be at least partially initialized
    # We check for basic attributes that indicate the MAVLink handshake has occurred
    timeout = 30
    start = time.time()
    while not vehicle.version:
        if time.time() - start > timeout:
            raise Exception("Timed out waiting for vehicle version")
        time.sleep(0.5)

    print("Successfully connected and initialized.")

    # 3. Read Health/Status Data
    print("-" * 30)
    print("Vehicle Health/Status:")
    # Use version to get system_id
    print(f"  System ID: {vehicle._master.mav.srcSystem}") 
    print(f"  Mode:      {vehicle.mode.name}")
    print(f"  Armed:     {vehicle.armed}")
    print(f"  Battery:   {vehicle.battery}")
    print(f"  GPS Fix:   {vehicle.gps_0.fix_type}")
    print(f"  EKF OK:    {vehicle.ekf_ok}")
    print("-" * 30)

    vehicle.close()
    print("Connection closed.")

if __name__ == "__main__":
    try:
        test_drone_connection()
    except Exception as e:
        print(f"Error: {e}")
