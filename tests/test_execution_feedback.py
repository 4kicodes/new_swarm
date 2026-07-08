import pytest
from swarm.planning import create_waypoint, create_route, build_execution_plan, CoordinateFrame
from swarm.execution import (
    create_execution, 
    start_execution, 
    execution_status,
    ExecutionStatus
)
from swarm.execution.feedback import FeedbackAdapter

class MockBus:
    def __init__(self):
        self.subscribers = {}
        self.published = []

    def subscribe(self, topic, callback):
        self.subscribers[topic] = callback

    def publish(self, topic, message):
        self.published.append((topic, message))

def test_feedback_pipeline():
    # Setup
    bus = MockBus()
    # Need access to registry - it's a singleton in api/manager
    from swarm.execution.api import _registry
    adapter = FeedbackAdapter(bus, _registry, acceptance_radius=2.0)
    
    # Create session
    wp1 = create_waypoint(10, 10, 100)
    wp2 = create_waypoint(10.00001, 10.00001, 100) # Inside 2m radius
    route = create_route([wp1, wp2])
    plan = build_execution_plan(route, CoordinateFrame.GLOBAL)
    
    sid = "test_feedback_sid"
    create_execution(sid, plan)
    
    # Start execution
    start_execution(sid)
    
    # Simulate telemetry update for wp1
    bus.subscribers["telemetry.position"]({"drone_id": "d1", "position": wp1})
    
    # Check advancement to waypoint 1
    assert execution_status(sid) == ExecutionStatus.RUNNING
    
    # Simulate telemetry update for wp2
    bus.subscribers["telemetry.position"]({"drone_id": "d1", "position": wp2})
    
    # Check completion
    assert execution_status(sid) == ExecutionStatus.COMPLETED
