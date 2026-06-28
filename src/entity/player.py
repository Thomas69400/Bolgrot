from ..BFS import BFS
from ..map import Map
from .entity import Entity, TypeEntity
from ..spells import Spells, LongJump, ShortJump, MoveFlames


class Player(Entity):
    def __init__(
            self,
            x: int = None,
            y: int = None,
            map: Map = None
    ):
        super().__init__()
        self.type_entity: TypeEntity = TypeEntity.PLAYER
        self.blocks_sight: bool = False
        self.pos_x: int | None = x
        self.pos_y: int | None = y
        self.hp: int = 40
        self.base_PA: int = 10
        self.pa: int = self.base_PA
        self.spells: list[Spells] = [
            ShortJump(bfs=BFS(map) if map is not None else None),
            LongJump(bfs=BFS(map) if map is not None else None),
            MoveFlames(bfs=BFS(map) if map is not None else None)
        ]
