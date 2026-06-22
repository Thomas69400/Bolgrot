from .spells import Spells, TypeSpell


class MoveFlames(Spells):
    def __init__(
            self,
            name: str = "Inaction",
            description: str = "",
            cost: int = 1,
            max_use: int = 1,
            effects: list[str] = [],
            type_spell: list[tuple[TypeSpell, int]] = [],
            line_of_sight: bool = False,
            sprite: str = "inaction.png"
    ):
        super().__init__(
            name, description, cost, max_use,
            effects, type_spell, line_of_sight, sprite)
        self.description: str = "Ennemies are attracted on the tile." \
            "Caster lose 5 HP." \
            "Ennemies can't kill the caster when using this spell."
        self.time_used: int = 0
        self.type_spell: list[tuple[TypeSpell, int]] = [
            (TypeSpell.DIAGONAL, 1)
        ]
        self.line_of_sight: bool = line_of_sight

    def play(self):
        pass

    def next_turn(self):
        self.time_used = 0
