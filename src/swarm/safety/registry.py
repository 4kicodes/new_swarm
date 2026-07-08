from typing import Dict, Optional, List
from .models import Constraint
from .exceptions import InvalidSafetyConfigurationError

class ConstraintRegistry:
    def __init__(self):
        self._constraints: Dict[str, Constraint] = {}

    def register_constraint(self, constraint: Constraint) -> None:
        if constraint.id in self._constraints:
            raise InvalidSafetyConfigurationError(f"Constraint {constraint.id} already registered.")
        self._constraints[constraint.id] = constraint

    def unregister_constraint(self, constraint_id: str) -> None:
        if constraint_id not in self._constraints:
            raise InvalidSafetyConfigurationError(f"Constraint {constraint_id} not found.")
        del self._constraints[constraint_id]

    def list_constraints(self) -> List[Constraint]:
        return list(self._constraints.values())

    def get_constraint(self, constraint_id: str) -> Optional[Constraint]:
        return self._constraints.get(constraint_id)
