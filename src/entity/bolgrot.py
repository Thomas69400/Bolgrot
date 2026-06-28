from .entity import Entity, TypeEntity


class Bolgrot(Entity):
    """The boss enemy. Occupies a tile and cannot be killed."""

    def __init__(
            self,
            x: int = None,
            y: int = None
    ):
        """Create Bolgrot at grid position (x, y); flagged unkillable."""
        super().__init__()
        self.type_entity: TypeEntity = TypeEntity.BOLGROT
        self.pos_x: int | None = x
        self.pos_y: int | None = y
        self.killable: bool = False
