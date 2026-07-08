import pytest
from swarm.planning import create_waypoint, create_route, build_execution_plan, CoordinateFrame, Waypoint, InvalidWaypointError
from swarm.safety import validate_execution_plan, Constraint, register_constraint, unregister_constraint, list_constraints

def test_valid_execution_plan():
    wp = create_waypoint(10, 10, 100)
    route = create_route([wp])
    plan = build_execution_plan(route, CoordinateFrame.GLOBAL)
    
    result = validate_execution_plan(plan)
    assert result.valid is True
    assert len(result.violations) == 0

def test_invalid_waypoint_altitude():
    # Planning model validation catches this before it reaches Safety
    with pytest.raises(InvalidWaypointError):
        create_waypoint(10, 10, -5)

def test_duplicate_waypoint():
    wp = create_waypoint(10, 10, 100)
    route = create_route([wp, wp])
    plan = build_execution_plan(route, CoordinateFrame.GLOBAL)
    
    result = validate_execution_plan(plan)
    assert result.valid is True # Warning only
    assert len(result.warnings) > 0
    assert any(w.code == "WARN_DUP_WP_1" for w in result.warnings)

def test_empty_route():
    with pytest.raises(Exception):
        create_route([])

def test_constraint_registry():
    c1 = Constraint("geofence", "Basic Geofence")
    register_constraint(c1)
    assert any(c.id == "geofence" for c in list_constraints())
    unregister_constraint("geofence")
    assert not any(c.id == "geofence" for c in list_constraints())
