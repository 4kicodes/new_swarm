import pytest
from swarm.formation import create_formation, get_status, FormationStatus, FormationType
from swarm.formation.exceptions import FormationNotFoundError

def test_lifecycle_transitions():
    f_id = "test_lifecycle"
    create_formation(f_id, "Test", FormationType.LINE)
    
    # Check initial status
    assert get_status(f_id) == FormationStatus.CREATED
