from .entity import Entity, TypeEntity


class Flame(Entity):
    def __init__(self):
        super().__init__()
        self.type_entity: TypeEntity = TypeEntity.FLAME
