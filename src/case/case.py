from ..entity import Entity
from enum import Enum


class CaseType(Enum):
    FREE = 0
    WALL = 1
    EMPTY = 2


class Case:
    def __init__(
        self,
        x: int,
        y: int,
        entity: Entity | None = None,
        case_type: CaseType = CaseType.FREE
    ) -> None:
        self.x = x
        self.y = y
        self.entity: Entity | None = entity
        self.case_type: CaseType = case_type
