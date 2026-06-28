from abc import ABC
from enum import Enum


class TypeEntity(Enum):
    """Discriminator used by the renderer to draw each entity kind."""
    NONE: int = 0
    FLAME: int = 1
    PLAYER: int = 2
    BOLGROT: int = 3


class Entity(ABC):
    """Abstract base for anything that can occupy a grid cell."""

    def __init__(self):
        """Initialise the shared entity flags (sight-blocking, killable)."""
        self.type_entity: TypeEntity | None = None
        self.blocks_sight: bool = True
        self.killable: bool = True
