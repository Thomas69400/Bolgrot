from __future__ import annotations
from ..entity import Bolgrot, Player, Flame, Entity
from .. import constant


class Map:
    def __init__(self) -> None:
        self.cases: dict[tuple[int, int], int | Entity] = {
            (i, j): 0
            for j in range(constant.GRID_MAX_Y)
            for i in range(constant.GRID_MAX_X)
        }
        base_x_p, base_y_p = constant.BASE_PLAYER_POS
        base_x_b, base_y_b = constant.BASE_BOLGROT_POS
        self.player: Player = Player(base_x_p, base_y_p)
        self.bolgrot: Bolgrot = Bolgrot(base_x_b, base_y_b)
        self.cases[(base_x_p, base_y_p)] = self.player
        self.cases[(base_x_b, base_y_b)] = self.bolgrot
        self.grid_max_x: int = constant.GRID_MAX_X
        self.grid_max_y: int = constant.GRID_MAX_Y
        self.cut_map()
        self.clean_map()

    def clean_map(self) -> None:
        new_cases: dict[tuple[int, int], int | Entity] = {}
        x_max: int = 0
        y_max: int = 0
        for (x, y), v in self.cases.items():
            nx, ny = x - 1, y - 2
            x_max = max(nx, x_max)
            y_max = max(ny, y_max)
            new_cases[(nx, ny)] = v
            if isinstance(v, Entity):
                v.pos_x, v.pos_y = nx, ny
        self.cases = new_cases
        self.grid_max_x = x_max
        self.grid_max_y = y_max

    def remove_left(self) -> None:
        i = 0
        for y in range(constant.GRID_MAX_Y - 1, constant.GRID_MAX_Y - 20, -1):
            i += 1
            for x in range(20 - i):
                self.cases.pop((x, y), None)

    def remove_top(self) -> None:
        for x in range(14):
            for y in range(14 - x):
                self.cases.pop((x, y), None)

    def remove_right(self) -> None:
        i = 0
        for x in range(constant.GRID_MAX_X - 1, 14, -1):
            i += 1
            for y in range(0, 24 - i):
                self.cases.pop((x, y), None)

    def remove_bottom(self) -> None:
        i = 0
        for y in range(constant.GRID_MAX_Y - 1, 20, -1):
            i += 1
            for x in range(20 + i, constant.GRID_MAX_X):
                self.cases.pop((x, y), None)

    def remove_extra(self) -> None:
        for coord in [
            (0, 14), (13, 1), (14, 1), (14, 0), (33, 20),
            *[(32, i) for i in range(19, 22)],
            *[(i, 32) for i in range(18, 22)],
            *[(i, 33) for i in range(19, 21)],
        ]:
            self.cases.pop(coord, None)

    def cut_map(self) -> None:
        self.remove_top()
        self.remove_left()
        self.remove_right()
        self.remove_bottom()
        self.remove_extra()

    def place_flames(self, pattern: list[tuple[int, int]]) -> None:
        for p in pattern:
            if p in self.cases:
                x, y = p
                self.cases[p] = Flame(x, y)
