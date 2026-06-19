from .entity import Entity, TypeEntity


class Flame(Entity):
    def __init__(
            self,
            x: int = None,
            y: int = None
    ) -> None:
        super().__init__()
        self.type_entity: TypeEntity = TypeEntity.FLAME
        self.pos_x: int | None = x
        self.pos_y: int | None = y
