from ..entity import TypeEntity
from .. import constant


class Map:
    def __init__(
            self
    ):
        self.cases: list[tuple[int, int]] = [
            [0 for j in range(constant.GRID_MAX_Y)]
            for i in range(constant.GRID_MAX_X)]
        self.cases[17][-3] = TypeEntity.BOLGROT
        self.cases[17][15] = TypeEntity.PLAYER
