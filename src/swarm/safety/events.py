from dataclasses import dataclass
from .models import Constraint

@dataclass(frozen=True)
class SafetyViolationDetected:
    violation_code: str
    severity: str

@dataclass(frozen=True)
class ValidationCompleted:
    valid: bool
    violation_count: int
