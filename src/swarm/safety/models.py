from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List

class Severity(Enum):
    INFO = auto()
    WARNING = auto()
    CRITICAL = auto()

@dataclass(frozen=True)
class Constraint:
    id: str
    name: str
    enabled: bool = True

@dataclass(frozen=True)
class SafetyViolation:
    code: str
    message: str
    severity: Severity

@dataclass(frozen=True)
class SafetyResult:
    valid: bool
    violations: List[SafetyViolation] = field(default_factory=list)
    warnings: List[SafetyViolation] = field(default_factory=list)
