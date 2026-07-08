import pytest
from swarm.formation.types import FormationType
from swarm.formation.geometry import generate_offsets
from swarm.formation.exceptions import InvalidFormationConfiguration

def test_line_geometry():
    offsets = generate_offsets(FormationType.LINE, "L1", ["F1", "F2"], 5.0)
    assert offsets["L1"].y == 0
    assert offsets["F1"].y == -5.0
    assert offsets["F2"].y == -10.0

def test_v_geometry():
    offsets = generate_offsets(FormationType.V, "L1", ["F1", "F2"], 5.0)
    # F1 (i=0): side=1, row=1 -> x=5, y=-5
    assert offsets["F1"].x == 5.0
    assert offsets["F1"].y == -5.0
    # F2 (i=1): side=-1, row=1 -> x=-5, y=-5
    assert offsets["F2"].x == -5.0
    assert offsets["F2"].y == -5.0

def test_validation():
    with pytest.raises(InvalidFormationConfiguration):
        generate_offsets(FormationType.LINE, "L1", ["F1"], -1.0) # Invalid spacing
    with pytest.raises(InvalidFormationConfiguration):
        generate_offsets(FormationType.LINE, "L1", ["L1", "F1"], 5.0) # Leader is follower
    with pytest.raises(InvalidFormationConfiguration):
        generate_offsets(FormationType.LINE, "L1", ["F1", "F1"], 5.0) # Duplicate followers
