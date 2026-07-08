import pytest
from swarm.commands.parser import parse
from swarm.commands.dispatcher import dispatch
from swarm.coordinator import create_session, get_status

class MockManager:
    pass

def test_coordinator_integration():
    create_session()
    manager = MockManager()
    
    # Simulate: create_formation f1 Test LINE
    cmd = parse("create_formation f1 Test LINE")
    dispatch(manager, cmd)
    
    # Check if coordinator session has the formation
    # The command handler calls coordinator.create_formation, which adds to registry.
    # Coordinator doesn't store formation_id in session, only active formation_id.
    # Need to load it.
    
    # Simulate: load_formation f1
    cmd = parse("load_formation f1")
    dispatch(manager, cmd)
    
    status = get_status()
    assert status["formation"] == "f1"
