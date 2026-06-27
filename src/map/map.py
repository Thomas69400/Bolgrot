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
        self.parse_map(map_conf)

    def parse_map(
        self,
        map_conf: str
    ) -> None:
        with open(map_conf, "r") as f:
            lines = [line.rstrip('\n').replace(" ", "")
                     for line in f if line.strip()]

        start_x: int = 0
        start_y: int = len(lines[0]) - 1
        for n_line, line in enumerate(lines):
            x: int = start_x
            y: int = start_y
            for symbol in line:
                if symbol == "N":
                    y -= 1
                    x += 1
                    continue
                self.cases.append(
                    Case(x, y, case_type=SYMBOL_MAP.get(symbol, CaseType.FREE)
                         ))
                x += 1
                y -= 1
            if n_line % 2 == 1:
                start_x += 1
            if n_line % 2 == 0:
                start_y += 1

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
