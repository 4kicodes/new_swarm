import math
import pytest
from swarm.planning import create_waypoint, distance, bearing, offset_waypoint, relative_position, Position, CoordinateFrame, convert_frame, create_route, route_length, route_bounding_box

def test_distance():
    w1 = create_waypoint(0, 0, 0)
    w2 = create_waypoint(0, 0, 0)
    assert distance(w1, w2) == 0.0
    
    w3 = create_waypoint(0, 1, 0) # ~111km
    assert distance(w1, w3) > 100000

def test_bearing():
    w1 = create_waypoint(0, 0, 0)
    w2 = create_waypoint(1, 0, 0) # North
    assert bearing(w1, w2) == 0.0
    
    w3 = create_waypoint(0, 1, 0) # East
    assert bearing(w1, w3) == 90.0

def test_offset_and_relative():
    w1 = create_waypoint(0, 0, 0)
    offset = Position(x=100, y=100, z=10)
    w2 = offset_waypoint(w1, offset)
    
    # Check inverse
    pos = relative_position(w1, w2)
    assert pos.x == pytest.approx(offset.x, abs=0.1)
    assert pos.y == pytest.approx(offset.y, abs=0.1)
    assert pos.z == pytest.approx(offset.z, abs=0.1)

def test_route_utils():
    w1 = create_waypoint(0, 0, 0)
    w2 = create_waypoint(0, 1, 0)
    r = create_route([w1, w2])
    
    assert route_length(r) > 100000
    
    min_lat, max_lat, min_lon, max_lon = route_bounding_box(r)
    assert min_lat == 0
    assert max_lat == 0
    assert min_lon == 0
    assert max_lon == 1

def test_frame_conversion():
    pos = Position(x=1, y=2, z=3)
    # NED to ENU
    converted = convert_frame(pos, CoordinateFrame.LOCAL_NED, CoordinateFrame.LOCAL_ENU)
    assert converted.x == 1
    assert converted.y == 2
    assert converted.z == 3
