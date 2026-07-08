import pytest
from swarm.planning import create_waypoint, create_route, build_execution_plan, CoordinateFrame
from swarm.execution import (
    create_execution, 
    start_execution, 
    pause_execution, 
    resume_execution, 
    advance_execution, 
    execution_status,
    ExecutionStatus
)
from swarm.execution.exceptions import InvalidTransitionError

def test_execution_lifecycle():
    wp = create_waypoint(10, 10, 100)
    route = create_route([wp, wp])
    plan = build_execution_plan(route, CoordinateFrame.GLOBAL)
    
    sid = "test_sid"
    create_execution(sid, plan)
    assert execution_status(sid) == ExecutionStatus.CREATED
    
    start_execution(sid)
    assert execution_status(sid) == ExecutionStatus.RUNNING
    
    pause_execution(sid)
    assert execution_status(sid) == ExecutionStatus.PAUSED
    
    resume_execution(sid)
    assert execution_status(sid) == ExecutionStatus.RUNNING
    
    advance_execution(sid) # Advance to waypoint 1
    advance_execution(sid) # Advance to waypoint 2 (completion)
    assert execution_status(sid) == ExecutionStatus.COMPLETED

def test_invalid_transition():
    wp = create_waypoint(10, 10, 100)
    route = create_route([wp])
    plan = build_execution_plan(route, CoordinateFrame.GLOBAL)
    
    sid = "test_sid_2"
    create_execution(sid, plan)
    
    # Cannot pause CREATED
    with pytest.raises(InvalidTransitionError):
        pause_execution(sid)
