from .spells import Spells, TypeSpell


class ShortJump(Spells):
    def __init__(
            self,
            name: str = "Astral leap",
            description: str = "",
            cost: int = 1,
            max_use: int = 99,
            effects: list[str] = [],
            type_spell: list[tuple[TypeSpell, int]] = [],
            line_of_sight: bool = True,
            sprite: str = "short_jump.png"
    ):
        super().__init__(
            name, description, cost, max_use,
            effects, type_spell, line_of_sight, sprite)
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
        self.type_spell: list[tuple[TypeSpell, int]] = [
            (TypeSpell.LINE, 1)
        ]

    def play(self):
        print(f"Playing spell: {self.name}")
        pass
