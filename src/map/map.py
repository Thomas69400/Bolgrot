from ..entity import TypeEntity
from .. import constant


class Map:
    def __init__(
            self
    ):
        self.cases: list[dict[tuple[int, int], int]] = [
            {(i, j): 0} for j in range(constant.GRID_MAX_Y)
            for i in range(constant.GRID_MAX_X)]
        for i, case in enumerate(self.cases):
            for k, v in case.items():
                x, y = k
                if x == 17 and y == constant.GRID_MAX_Y - 4:
                    self.cases[i].update({k: TypeEntity.BOLGROT})
                elif x == 17 and y == 15:
                    self.cases[i].update({k: TypeEntity.PLAYER})
        self.cut_map()

    def cpy_cases(self) -> list[dict[tuple[int, int], int]]:
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
