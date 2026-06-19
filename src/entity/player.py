from .entity import Entity, TypeEntity


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
