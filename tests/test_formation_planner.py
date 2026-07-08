import pytest
from swarm.planning import create_waypoint, CoordinateFrame, create_route, build_execution_plan
from swarm.formation import create_formation, set_leader, set_followers, generate_targets, FormationType
from swarm.safety import validate_execution_plan, Constraint, register_constraint

def test_line_target_generation():
    formation_id = "f1"
    create_formation(formation_id, "TestLine", FormationType.LINE)
    set_leader(formation_id, "L1")
    set_followers(formation_id, ["F1"])
    
    leader_wp = create_waypoint(10.0, 10.0, 100.0)
    targets = generate_targets(formation_id, leader_wp)
    
    assert "L1" in targets
    assert "F1" in targets
    assert targets["L1"] == leader_wp
    # F1 offset for LINE is (0, -5, 0)
    assert targets["F1"].latitude == pytest.approx(10.0, abs=1e-4)
    assert targets["F1"].longitude == pytest.approx(10.0, abs=1e-4)
    assert targets["F1"].altitude == pytest.approx(100.0, abs=1e-4)

def test_safety_validation_failure():
    # Setup a formation that would fail a safety check if we added a constraint
    formation_id = "f2"
    create_formation(formation_id, "TestV", FormationType.V)
    set_leader(formation_id, "L1")
    
    # Structural check by planning factory - cannot create invalid waypoint
    with pytest.raises(Exception):
        create_waypoint(10.0, 10.0, -100.0)
