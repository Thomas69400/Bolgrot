from .entity import Entity, TypeEntity


class Player(Entity):
    def __init__(self):
        super().__init__()
        self.type_entity: TypeEntity = TypeEntity.PLAYER
