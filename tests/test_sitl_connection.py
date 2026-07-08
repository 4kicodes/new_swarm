from dronekit import connect
import time

endpoints = ['udpin:0.0.0.0:14550', 'udpin:0.0.0.0:14560', 'udpin:0.0.0.0:14570']

def test_connections():
    results = {}
    for ep in endpoints:
        print(f"Connecting to {ep}...")
        try:
            # Short timeout to quickly identify dead endpoints
            vehicle = connect(ep, wait_ready=False, heartbeat_timeout=5)
            # Give it a bit of time to establish MAVLink heartbeat
            time.sleep(3)
            if vehicle.version:
                results[ep] = f"SUCCESS: {vehicle.version}"
            else:
                results[ep] = "FAILED: No version info (heartbeat issue)"
            vehicle.close()
        except Exception as e:
            results[ep] = f"FAILED: {str(e)}"
    
    print("\n--- Connection Report ---")
    for ep, status in results.items():
        print(f"{ep}: {status}")

if __name__ == "__main__":
    test_connections()
