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

    def remove_line(self):
        pass

    def remove_left(self):
        for x in range(4):
            for y in range(4 - x):
                self.cases[x].pop()

    def remove_top(self):
        for y in range(constant.GRID_MAX_Y, 3, -1):
            for x in range(2):
                self.cases[x].pop()

    def cut_map(self):
        # self.remove_left()
        self.remove_top()
