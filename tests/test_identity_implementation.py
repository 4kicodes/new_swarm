from unittest.mock import MagicMock
from swarm.drone.identity import DroneIdentity

def test_drone_identity_creation():
    # Mock mavutil.mavlink_connection master
    mock_master = MagicMock()
    mock_master.target_system = 5
    mock_master.target_component = 1
    
    identity = DroneIdentity.from_mavlink_master(mock_master)
    
    assert identity.system_id == 5
    assert identity.component_id == 1
    assert identity.name == "drone_5"
    print("Verification Successful: DroneIdentity created correctly from mock master.")

if __name__ == "__main__":
    try:
        test_drone_identity_creation()
    except Exception as e:
        print(f"Verification Failed: {e}")
        exit(1)
