from .entity import Entity, TypeEntity


class Bolgrot(Entity):
    def __init__(self):
        super().__init__()
        self.type_entity: TypeEntity = TypeEntity.BOLGROT
