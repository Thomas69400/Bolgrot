from .entity import Entity, TypeEntity


class Bolgrot(Entity):
    def __init__(
            self,
            x: int = None,
            y: int = None
    ):
        super().__init__()
        self.type_entity: TypeEntity = TypeEntity.BOLGROT
        self.pos_x: int | None = x
        self.pos_y: int | None = y
        self.killable: bool = False
