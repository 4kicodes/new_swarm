import pytest
from swarm.planning import create_waypoint
from swarm.formation import create_formation, set_leader, set_followers, FormationType
from swarm.mission import create_mission, assign_formation, MissionType
from swarm.coordinator import orchestrate_mission

def test_full_pipeline_orchestration():
    # Setup domains
    f_id = "f_pipeline"
    create_formation(f_id, "Pipeline Formation", FormationType.LINE)
    set_leader(f_id, "L1")
    set_followers(f_id, ["F1"])
    
    m_id = "m_pipeline"
    create_mission(m_id, "Pipeline Mission", MissionType.WAYPOINT)
    assign_formation(m_id, f_id)
    
    # Orchestrate
    leader_wp = create_waypoint(10.0, 10.0, 100.0)
    session = orchestrate_mission(m_id, leader_wp)
    
    assert session is not None
    assert session.session_id == f"session_{m_id}"
    assert len(session.execution_plan.trajectory) == 2 # L1 + F1
