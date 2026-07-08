import pytest
from swarm.planning import create_waypoint, create_route, append_waypoint, prepend_waypoint, merge_routes, reverse_route, copy_route

def test_route_immutability_and_operations():
    w1 = create_waypoint(0, 0, 0)
    w2 = create_waypoint(1, 1, 1)
    r1 = create_route([w1])
    
    # Test append
    r2 = append_waypoint(r1, w2)
    assert len(r1.waypoints) == 1
    assert len(r2.waypoints) == 2
    
    # Test prepend
    r3 = prepend_waypoint(r1, w2)
    assert len(r1.waypoints) == 1
    assert len(r3.waypoints) == 2
    
    # Test merge
    r4 = merge_routes(r1, r2)
    assert len(r4.waypoints) == 3
    
    # Test reverse
    r5 = reverse_route(r4)
    assert r5.waypoints[0] == r4.waypoints[-1]
    
    # Test copy
    r6 = copy_route(r1)
    assert r6 == r1
    assert r6 is not r1
