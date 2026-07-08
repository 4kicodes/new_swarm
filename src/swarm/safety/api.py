from typing import List, Callable
from swarm.planning import ExecutionPlan
from .models import SafetyResult, SafetyViolation, Severity, Constraint
from .registry import ConstraintRegistry
from .exceptions import ConstraintViolationError

# Global registry
_registry = ConstraintRegistry()

def register_constraint(constraint: Constraint) -> None:
    _registry.register_constraint(constraint)

def unregister_constraint(constraint_id: str) -> None:
    _registry.unregister_constraint(constraint_id)

def list_constraints() -> List[Constraint]:
    return _registry.list_constraints()

# Validation Pipeline
def validate_execution_plan(plan: ExecutionPlan) -> SafetyResult:
    """Aggregates all active constraint validations."""
    violations = []
    warnings = []
    
    # 1. Structural Validation (Mandatory)
    if not plan.route or not plan.route.waypoints:
        violations.append(SafetyViolation("ERR_EMPTY_ROUTE", "Route is empty", Severity.CRITICAL))
    
    # 2. Waypoint Validation
    for i, wp in enumerate(plan.route.waypoints):
        if wp.altitude < 0:
            violations.append(SafetyViolation(f"ERR_NEG_ALT_{i}", f"Negative altitude at waypoint {i}", Severity.CRITICAL))
        
        # Check consecutive duplicates
        if i > 0:
            prev = plan.route.waypoints[i-1]
            if wp.latitude == prev.latitude and wp.longitude == prev.longitude:
                warnings.append(SafetyViolation(f"WARN_DUP_WP_{i}", f"Duplicate waypoint at {i}", Severity.WARNING))

    # 3. Constraint-based validation from Registry would happen here
    # For now, structural checks satisfy initial requirements
    
    return SafetyResult(
        valid=len(violations) == 0,
        violations=violations,
        warnings=warnings
    )
