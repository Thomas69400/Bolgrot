from abc import ABC
from enum import Enum


class TypeEntity(Enum):
    NONE: int = 0
    FLAME: int = 1
    PLAYER: int = 2
    BOLGROT: int = 3


class Entity(ABC):
    def __init__(self):
        self.type_entity: TypeEntity | None = None
        self.blocks_sight: bool = True
        self.killable: bool = True
