from .entity import Entity, TypeEntity
from ..spells import Spells, LongJump, ShortJump, MoveFlames


class Player(Entity):
    def __init__(
            self,
            x: int = None,
            y: int = None
    ):
        super().__init__()
        self.type_entity: TypeEntity = TypeEntity.PLAYER
        self.pos_x: int | None = x
        self.pos_y: int | None = y
        self.hp: int = 40
        self.base_PA: int = 10
        self.spells: list[Spells] = [
            ShortJump(),
            LongJump(),
            MoveFlames()
        ]
