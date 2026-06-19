from ..entity import Bolgrot, Player, Flame, Entity
from .. import constant


class Map:
    def __init__(
            self
    ):
        self.cases: list[dict[tuple[int, int], int | Entity]] = [
            {(i, j): 0} for j in range(constant.GRID_MAX_Y)
            for i in range(constant.GRID_MAX_X)]
        self.player: Player = Player(16, 15)
        self.bolgrot: Bolgrot = Bolgrot(21, 10)
        for i, case in enumerate(self.cases):
            for k, v in case.items():
                x, y = k
                if x == 21 and y == 10:
                    self.cases[i].update({k: self.bolgrot})
                elif x == 16 and y == 15:
                    self.cases[i].update({k: self.player})
        self.cut_map()
        self.clean_map()

    def clean_map(self):
        cpy: list[dict[tuple[int, int], int | Entity]] = []
        for case in self.cases:
            for k, v in case.items():
                x, y = k
                cpy.append({(x - 1, y - 2): v})
        self.cases = cpy

    def cpy_cases(self) -> list[dict[tuple[int, int], int | Entity]]:
        new_cases: list[dict[tuple[int, int], int]] = []
        for case in self.cases:
            new_cases.append(case.copy())
        return new_cases

    def remove_left(self) -> None:
        cpy: list[dict[tuple[int, int], int]] = self.cpy_cases()
        i = 0
        for y in range(constant.GRID_MAX_Y - 1, constant.GRID_MAX_Y - 20, -1):
            i += 1
            for x in range(20 - i):
                cpy.remove({(x, y): 0})
        self.cases = cpy

    def remove_top(self) -> None:
        cpy: list[dict[tuple[int, int], int]] = self.cpy_cases()
        for x in range(14):
            for y in range(14 - x):
                cpy.remove({(x, y): 0})
        self.cases = cpy

    def remove_right(self) -> None:
        cpy: list[dict[tuple[int, int], int]] = self.cpy_cases()
        i = 0
        for x in range(constant.GRID_MAX_X - 1, 14, -1):
            i += 1
            for y in range(0, 24 - i):
                cpy.remove({(x, y): 0})
        self.cases = cpy

    def remove_bottom(self) -> None:
        cpy: list[dict[tuple[int, int], int]] = self.cpy_cases()
        i = 0
        for y in range(constant.GRID_MAX_Y - 1, 20, -1):
            i += 1
            for x in range(20 + i, constant.GRID_MAX_X):
                try:
                    cpy.remove({(x, y): 0})
                except Exception:
                    continue
        self.cases = cpy

    def remove_extra(self) -> None:
        self.cases.remove({(0, 14): 0})
        self.cases.remove({(13, 1): 0})
        self.cases.remove({(14, 1): 0})
        self.cases.remove({(14, 0): 0})
        self.cases.remove({(33, 20): 0})
        for i in range(19, 22):
            self.cases.remove({(32, i): 0})
        for i in range(18, 22):
            self.cases.remove({(i, 32): 0})
        for i in range(19, 21):
            self.cases.remove({(i, 33): 0})

    def cut_map(self) -> None:
        self.remove_top()
        self.remove_left()
        self.remove_right()
        self.remove_bottom()
        self.remove_extra()

    def place_flames(
            self,
            pattern: list[list[tuple[int, int]]]
    ) -> None:
        for p in pattern:
            for i, case in enumerate(self.cases):
                for k, v in case.items():
                    if k == p:
                        x, y = k
                        self.cases[i].update({k: Flame(x, y)})
