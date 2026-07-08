import pytest
from swarm.planning import create_waypoint, create_route, Waypoint, InvalidWaypointError, InvalidRouteError, CoordinateFrame, build_execution_plan

def test_waypoint_validation():
    # Valid
    create_waypoint(0, 0, 0)
    create_waypoint(90, 180, 100)
    
    # Invalid lat
    with pytest.raises(InvalidWaypointError):
        create_waypoint(91, 0, 0)
    
    # Invalid lon
    with pytest.raises(InvalidWaypointError):
        create_waypoint(0, 181, 0)
        
    # Invalid alt
    with pytest.raises(InvalidWaypointError):
        create_waypoint(0, 0, -1)

def test_route_validation():
    # Valid
    w1 = create_waypoint(0, 0, 0)
    create_route([w1])
    
    # Empty
    with pytest.raises(InvalidRouteError):
        create_route([])

def test_execution_plan_creation():
    w1 = create_waypoint(0, 0, 0)
    r1 = create_route([w1])
    # Build plan through service
    plan = build_execution_plan(r1, CoordinateFrame.GLOBAL)
    assert len(plan.trajectory) == 1
    assert plan.frame == CoordinateFrame.GLOBAL
