from abc import ABC, abstractmethod
from enum import Enum


class Direction(Enum):
    NORTH: tuple = (-1, 0)
    EAST: tuple = (0, 1)
    SOUTH: tuple = (1, 0)
    WEST: tuple = (0, -1)

    DIRECTIONS: list[tuple] = [
        NORTH,
        EAST,
        SOUTH,
        WEST
    ]


class Spells(ABC):
    def __init__(
            self,
            name: str,
            description: str,
            cost: int,
            max_use: int,
            effects: list[str],
            sprite=None
    ):
        super().__init__()
        self.sprite = sprite
        self.name: str = name
        self.description: str = description
        self.cost: int = cost
        self.max_use: int = max_use
        self.effects: list[str] = effects

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def previsu(self):
        pass

    @staticmethod
    def is_in_map(
        pos_spell: tuple,
        cases: list[dict[tuple, int]],
    ) -> bool:
        for c in cases:
            for k, v in c.items():
                if k == pos_spell:
                    return True
        return False
