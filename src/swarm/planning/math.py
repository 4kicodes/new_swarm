import math
from typing import Tuple
from .models import Waypoint, Position, Route, CoordinateFrame
from .exceptions import PlanningError

# Earth radius in meters
EARTH_RADIUS = 6371000.0

def distance(a: Waypoint, b: Waypoint) -> float:
    """Calculates ground distance in meters between two Waypoints using Haversine."""
    lat1, lon1 = math.radians(a.latitude), math.radians(a.longitude)
    lat2, lon2 = math.radians(b.latitude), math.radians(b.longitude)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    h = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    return 2 * EARTH_RADIUS * math.asin(math.sqrt(h))

def bearing(a: Waypoint, b: Waypoint) -> float:
    """Calculates initial bearing in degrees between two Waypoints."""
    lat1, lon1 = math.radians(a.latitude), math.radians(a.longitude)
    lat2, lon2 = math.radians(b.latitude), math.radians(b.longitude)
    
    y = math.sin(lon2 - lon1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
    
    brng = math.degrees(math.atan2(y, x))
    return (brng + 360) % 360

def offset_waypoint(origin: Waypoint, offset: Position) -> Waypoint:
    """
    Computes a new Waypoint given an origin and local NED/ENU offset.
    Position.x (East), Position.y (North), Position.z (Altitude offset)
    """
    # Simple Earth approximation for small offsets
    lat_rad = math.radians(origin.latitude)
    
    # Delta lat/lon in radians
    dlat = offset.y / EARTH_RADIUS
    dlon = offset.x / (EARTH_RADIUS * math.cos(lat_rad))
    
    new_lat = origin.latitude + math.degrees(dlat)
    new_lon = origin.longitude + math.degrees(dlon)
    new_alt = origin.altitude + offset.z
    
    from .api import create_waypoint
    return create_waypoint(new_lat, new_lon, new_alt)

def relative_position(origin: Waypoint, target: Waypoint) -> Position:
    """Returns local offset (x=East, y=North, z=Altitude) between two Waypoints."""
    lat_rad = math.radians(origin.latitude)
    
    dlat = math.radians(target.latitude - origin.latitude)
    dlon = math.radians(target.longitude - origin.longitude)
    
    y = dlat * EARTH_RADIUS
    x = dlon * EARTH_RADIUS * math.cos(lat_rad)
    z = target.altitude - origin.altitude
    
    return Position(x=x, y=y, z=z)

def route_length(route: Route) -> float:
    """Cumulative distance of a route."""
    length = 0.0
    for i in range(len(route.waypoints) - 1):
        length += distance(route.waypoints[i], route.waypoints[i+1])
    return length

def route_bounding_box(route: Route) -> Tuple[float, float, float, float]:
    """Returns (min_lat, max_lat, min_lon, max_lon)."""
    lats = [w.latitude for w in route.waypoints]
    lons = [w.longitude for w in route.waypoints]
    return (min(lats), max(lats), min(lons), max(lons))

def convert_frame(pos: Position, from_frame: CoordinateFrame, to_frame: CoordinateFrame) -> Position:
    """Simple coordinate frame transform."""
    if from_frame == to_frame:
        return pos
    
    # Basic NED <-> ENU: (N, E, D) <-> (E, N, U)
    # Mapping x=East, y=North, z=Altitude
    if from_frame == CoordinateFrame.LOCAL_NED and to_frame == CoordinateFrame.LOCAL_ENU:
        return Position(x=pos.x, y=pos.y, z=pos.z) # NED x is North, y is East; ENU x is East, y is North
    
    raise PlanningError(f"Conversion from {from_frame} to {to_frame} not implemented.")
