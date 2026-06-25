from __future__ import annotations
from ..entity import Entity
from .. import constant
from ..case import Case, CaseType

SYMBOL_MAP = {
    '.': CaseType.FREE,
    '#': CaseType.WALL,
    "|": CaseType.EMPTY,
    "N": None
}


class Map:
    def __init__(
        self,
        map_conf: str = constant.MAP_CONF,
    ) -> None:
        self.cases: list[Case] = []
        self.player_spawn: tuple[int, int] | None = None
        self.bolgrot_spawn: tuple[int, int] | None = None
        self.parse_map(map_conf)

    def parse_map(
        self,
        map_conf: str
    ) -> None:
        with open(map_conf, "r") as f:
            lines = [line.rstrip('\n').replace(" ", "") for line in f if line.strip()]

        len_lines = len(lines[0])
        start_x = 0
        for n_line in range(len(lines)):
            n_N = 0
            print(f"Line {n_line}: {lines[n_line]}")
            for n_char, char in enumerate(lines[n_line]):
                if char == "N":
                    n_N += 1
                    continue
                elif len(char) != 1 or char not in SYMBOL_MAP:
                    raise ValueError(
                        f"Invalid character '{char}' in map config.")

                print(n_line, n_char, char, n_N)
                if n_char < len_lines - n_line - 1:
                    x = n_char - n_N
                else:
                    x = start_x
                y = len_lines - n_char
                print(f"Adding case at ({x}, {y}) with type {SYMBOL_MAP[char]}")
                self.cases.append(Case(x, y, SYMBOL_MAP[char]))
            start_x += 1

        self.grid_max_x = max(case.x for case in self.cases)
        self.grid_max_y = max(case.y for case in self.cases)

    def place_entity(
        self,
        pattern: list[tuple[int, int]],
        entity: Entity
    ) -> None:
        if not isinstance(entity, Entity):
            raise ValueError(
                "Entity must be an instance of Bolgrot or Player.")
        for x, y in pattern:
            for case in self.cases:
                if (case.x, case.y) == (x, y):
                    case.entity = entity
                    return
        raise ValueError(
            f"Invalid position ({entity.pos_x}, "
            f"{entity.pos_y}) for entity {entity}. No matching case found.")
