from .spells import Spells


class MoveFlames(Spells):
    def __init__(
            self,
            name: str = "Inaction",
            description: str = "",
            cost: int = 1,
            max_use: int = 1,
            effects: list[str] = [],
            sprite: str = "inaction.xcf"
    ):
        super().__init__(
            name, description, cost, max_use, effects, sprite)
        self.description: str = "Ennemies are attracted on the tile." \
            "Caster lose 5 HP." \
            "Ennemies can't kill the caster when using this spell."
        self.time_used: int = 0

    def play(self):
        pass

    def next_turn(self):
        self.time_used = 0
