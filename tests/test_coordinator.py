import pytest
from swarm.coordinator import create_session, load_mission, load_formation, get_status, generate_execution_plan, validate_plan
from swarm.mission import create_mission
from swarm.formation import create_formation, FormationType
from swarm.planning import create_waypoint

def test_session_lifecycle():
    create_session()
    
    # Setup domains
    create_mission("m1", "M1", None)
    create_formation("f1", "F1", FormationType.LINE)
    
    load_mission("m1")
    load_formation("f1")
    
    status = get_status()
    assert status["mission"] == "m1"
    assert status["formation"] == "f1"

def test_execution_plan_building():
    create_session()
    
    create_mission("m2", "M2", None)
    create_formation("f2", "F2", FormationType.LINE)
    
    load_mission("m2")
    load_formation("f2")
    
    wp = create_waypoint(10.0, 10.0, 100.0)
    plan = generate_execution_plan(wp)
    assert plan is not None
    
    result = validate_plan(plan)
    assert result.valid is True
