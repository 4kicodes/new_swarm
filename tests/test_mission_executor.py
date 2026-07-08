import pytest
from swarm.planning import create_waypoint, Waypoint
from swarm.formation import create_formation, set_leader, set_followers, FormationType
from swarm.mission import create_mission, attach_plan, start, execute_next_goal, MissionType, MissionGoal, MissionPlan, assign_formation

def test_mission_flow():
    # Setup
    formation_id = "f1"
    create_formation(formation_id, "Formation", FormationType.LINE)
    set_leader(formation_id, "L1")
    set_followers(formation_id, ["F1"])
    
    m_id = "m1"
    create_mission(m_id, "Mission", MissionType.WAYPOINT)
    assign_formation(m_id, formation_id)
    
    goal1 = MissionGoal("g1", create_waypoint(10.0, 10.0, 100.0))
    plan = MissionPlan(goals=[goal1])
    attach_plan(m_id, plan)
    
    # Start and execute
    plan = start(m_id)
    assert plan is not None
    assert len(plan.trajectory) == 2 # L1 + F1
    
    # Try next goal - should be none
    next_plan = execute_next_goal(m_id)
    assert next_plan is None
