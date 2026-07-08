from dataclasses import dataclass

@dataclass(frozen=True)
class FormationCreated:
    formation_id: str

@dataclass(frozen=True)
class FormationUpdated:
    formation_id: str

@dataclass(frozen=True)
class FormationActivated:
    formation_id: str

@dataclass(frozen=True)
class FormationDeleted:
    formation_id: str
