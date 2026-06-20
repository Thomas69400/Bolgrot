from .spells import Spells


class ShortJump(Spells):
    def __init__(
            self,
            name: str = "Astral leap",
            description: str = "",
            cost: int = 1,
            max_use: int = 99,
            effects: list[str] = [],
            sprite=None
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
            "after the teleportation." \
            "If an ennemy can't be moved, you die."

    def play(self):
        pass
