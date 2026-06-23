from abc import ABC, abstractmethod
from enum import Enum


class Direction(Enum):
    NORTH: tuple = (-1, 0)
    EAST: tuple = (0, 1)
    SOUTH: tuple = (1, 0)
    WEST: tuple = (0, -1)

    NORTH_WEST: tuple = (-1, -1)
    NORTH_EAST: tuple = (-1, 1)
    SOUTH_WEST: tuple = (1, -1)
    SOUTH_EAST: tuple = (1, 1)

    DIRECTIONS_LINE: list[tuple] = [
        NORTH,
        EAST,
        SOUTH,
        WEST
    ]

    DIRECTIONS_DIAGONALS: list[tuple] = [
        NORTH_WEST,
        NORTH_EAST,
        SOUTH_WEST,
        SOUTH_EAST
    ]


class TypeSpell(Enum):
    LINE: int = 2
    DIAGONAL: int = 4
    FULL: int = 8


class Spells(ABC):
    def __init__(
            self,
            name: str,
            description: str,
            cost: int,
            max_use: int,
            effects: list[str],
            type_spell: list[tuple[TypeSpell, int]],
            line_of_sight: bool = True,
            sprite=None
    ):
        super().__init__()
        self.sprite = sprite
        self.name: str = name
        self.description: str = description
        self.cost: int = cost
        self.max_use: int = max_use
        self.effects: list[str] = effects
        self.type_spell: list[tuple[TypeSpell, int]] = type_spell
        self.line_of_sight: bool = line_of_sight
        self.sprite = sprite

    @abstractmethod
    def play(self):
        pass

    def previsu(
        self,
        pos_player: tuple[int, int],
        cases: dict
    ) -> list[tuple]:
        all_pos: list[tuple] = []
        for type_s in self.type_spell:
            t, r = type_s
            match t.value:
                case 2:
                    all_pos.extend(self.make_line(
                        pos_player,
                        cases,
                        r
                    ))
                case 4:
                    all_pos.extend(self.make_diag(
                        pos_player,
                        cases,
                        r
                    ))
                case 8:
                    print("FULL")
        return all_pos

    def make_line(
        self,
        pos_player: tuple[int, int],
        cases: dict,
        range_s: int
    ) -> list[tuple]:
        x, y = pos_player
        possible_pos: list[tuple] = []
        try:
            for direction in Direction.DIRECTIONS_LINE.value:
                dx, dy = direction
                nx, ny = x, y
                for i in range(range_s):
                    nx, ny = nx + dx, ny + dy
                    if self.is_in_map((nx, ny), cases) and \
                            not self.is_blocked_by_sight(
                                (nx, ny), cases, direction):
                        possible_pos.append((nx, ny))
            return possible_pos
        except Exception:
            return []

    def make_diag(
        self,
        pos_player: tuple[int, int],
        cases: dict,
        range_s: int
    ) -> list[tuple]:
        x, y = pos_player
        possible_pos: list[tuple] = []
        try:
            for direction in Direction.DIRECTIONS_DIAGONALS.value:
                dx, dy = direction
                nx, ny = x, y
                for i in range(range_s):
                    nx, ny = nx + dx, ny + dy
                    if self.is_in_map((nx, ny), cases) and \
                            not self.is_blocked_by_sight(
                                (nx, ny), cases, direction):
                        possible_pos.append((nx, ny))
            return possible_pos
        except Exception:
            return []

    def is_blocked_by_sight(
        self,
        pos_spell: tuple,
        cases: dict,
        direction: Direction,
    ) -> bool:
        """Check if the spell is blocked by a wall or obstacle."""
        from ..entity import Player
        if self.line_of_sight is False:
            return False

        dx, dy = direction
        dx, dy = -1 * dx, -1 * dy
        nx, ny = pos_spell[0] + dx, pos_spell[1] + dy
        for case in cases:
            if ((nx, ny) == case and
                    (cases[case] != 0 and
                     not isinstance(cases[case], Player))):
                return True
        return False

    def is_in_map(
        self,
        pos_spell: tuple,
        cases: dict
    ) -> bool:
        return pos_spell in cases
