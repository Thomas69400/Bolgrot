from .spells import Spells


class LongJump(Spells):
    def __init__(
            self,
            name: str = "Double leap",
            description: str = "",
            cost: int = 2,
            max_use: int = 2,
            effects: list[str] = [],
            sprite: str = "long_jump.xcf"
    ):
        super().__init__(
            name, description, cost, max_use, effects, sprite)
        self.effects: list[str] = [
            "Teleport to the tile",
            "Attract 1 tile",
            "-1 Vit"
        ]
        self.description: str = "Teleport to the tile." \
            "Lose 1 HP." \
            "Can be use on an occupied tile to kill ennemy." \
            "If an ennemy is killed, restore 1 HP." \
            "All ennemies are attracted towards the caster" \
            " after the teleportation." \
            "If an ennemy can't be moved, you die."
        self.time_used: int = 0

    def play(self):
        pass

    def previsu(self):
        pass

    def next_turn(self):
        self.time_used = 0
