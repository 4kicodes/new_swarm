from loguru import logger
from swarm.messaging.topics import TOPIC_DRONE_HEALTH

# Keep track of known drones outside of a class
_known_drones = set()

def collect_telemetry(manager, bus, console_state):
    """
    Collect and publish telemetry data from the swarm.
    """
    swarm_telemetry = {"drones": {}, "connected_count": 0, "warning_count": 0}
    current_drones = manager.get_drones()
    current_drone_ids = set(current_drones.keys())
    
    # Detect disconnects
    for drone_id in _known_drones - current_drone_ids:
        console_state.events.append(f"Disconnected {drone_id}")
        _known_drones.remove(drone_id)

    for drone_id, vehicle in current_drones.items():
        try:
            # Extract health data
            armed = vehicle.armed
            mode = vehicle.mode.name if vehicle.mode else "N/A"
            battery = vehicle.battery.level if vehicle.battery else None
            gps_fix = vehicle.gps_0.fix_type if vehicle.gps_0 else None
            
            # Publish Health Event
            bus.publish(TOPIC_DRONE_HEALTH, {
                "drone_id": drone_id,
                "battery_percentage": battery,
                "gps_fix": gps_fix,
                "ekf_ok": True,
                "armed": armed,
                "mode": mode
            })

            # Extract telemetry data
            swarm_telemetry["drones"][drone_id] = {
                "drone_id": drone_id,
                "connected": True,
                "mode": mode,
                "armed": armed,
                "altitude": vehicle.location.global_relative_frame.alt if vehicle.location and vehicle.location.global_relative_frame else None,
                "battery_percentage": battery,
                "battery_voltage": vehicle.battery.voltage if vehicle.battery else None,
                "gps_fix": gps_fix,
                "satellites": vehicle.gps_0.satellites_visible if vehicle.gps_0 else None,
            }
            
            if drone_id not in _known_drones:
                console_state.events.append(f"Connected {drone_id}")
                _known_drones.add(drone_id)

        except Exception as e:
            logger.error(f"Failed to collect telemetry for {drone_id}: {e}")
            console_state.events.append(f"Warning: Telemetry error {drone_id}")
            swarm_telemetry["warning_count"] += 1
    
    swarm_telemetry["connected_count"] = len(swarm_telemetry["drones"])
    console_state.swarm = swarm_telemetry
