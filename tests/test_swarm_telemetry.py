import pytest
import threading
import time
from swarm.messaging.bus import InMemoryBus
from swarm.messaging.events import DronePositionEvent, ConnectionEvent
from swarm.messaging.monitors.position_monitor import PositionMonitor
from swarm.messaging.topics import TOPIC_DRONE_POSITION, TOPIC_DRONE_CONNECTION

def test_drone_position_event_creation():
    event = DronePositionEvent(
        drone_id="drone_1",
        latitude=10.0,
        longitude=20.0,
        altitude_msl=50.0,
        relative_altitude=5.0,
        heading=90.0,
        ground_speed=10.0
    )
    assert event.drone_id == "drone_1"
    assert event.vx == 0.0

def test_bus_and_publisher():
    bus = InMemoryBus()
    received = []
    
    def callback(event):
        received.append(event)
    
    bus.subscribe(TOPIC_DRONE_POSITION, callback)
    
    event = DronePositionEvent("drone_1", 10.0, 20.0, 50.0, 5.0, 90.0, 10.0)
    bus.publish(TOPIC_DRONE_POSITION, event)
    
    assert len(received) == 1
    assert received[0].drone_id == "drone_1"

def test_position_monitor_logic():
    bus = InMemoryBus()
    monitor = PositionMonitor(bus)
    
    event = DronePositionEvent("drone_1", 10.0, 20.0, 50.0, 5.0, 90.0, 10.0)
    bus.publish(TOPIC_DRONE_POSITION, event)
    
    time.sleep(0.1) # Allow for async processing if needed, though InMemoryBus is sync
    
    assert monitor.get_position("drone_1").latitude == 10.0
    
    # Update position
    event_update = DronePositionEvent("drone_1", 11.0, 21.0, 51.0, 6.0, 91.0, 11.0)
    bus.publish(TOPIC_DRONE_POSITION, event_update)
    
    assert monitor.get_position("drone_1").latitude == 11.0
    assert len(monitor.get_all_positions()) == 1

def test_position_monitor_cleanup():
    bus = InMemoryBus()
    monitor = PositionMonitor(bus)
    
    # Add position
    event = DronePositionEvent("drone_1", 10.0, 20.0, 50.0, 5.0, 90.0, 10.0)
    bus.publish(TOPIC_DRONE_POSITION, event)
    
    # Disconnect
    disconnect_event = ConnectionEvent("drone_1", "disconnected")
    bus.publish(TOPIC_DRONE_CONNECTION, disconnect_event)
    
    assert monitor.get_position("drone_1") is None

def test_position_monitor_thread_safety():
    bus = InMemoryBus()
    monitor = PositionMonitor(bus)
    
    def update_task():
        for i in range(100):
            event = DronePositionEvent("drone_1", float(i), 20.0, 50.0, 5.0, 90.0, 10.0)
            bus.publish(TOPIC_DRONE_POSITION, event)
            
    threads = [threading.Thread(target=update_task) for _ in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    assert len(monitor.get_all_positions()) == 1
