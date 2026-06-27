from __future__ import annotations
from typing import TYPE_CHECKING
from .spells import Spells, TypeSpell

if TYPE_CHECKING:
    from ..entity import Player, Bolgrot
    from ..map import Map


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

    def play(
        self,
        map: Map,
        player: Player,
        tile_clicked: tuple[int, int],
    ) -> None:
        if tile_clicked not in self.previsu(
                (player.pos_x, player.pos_y), map.cases):
            return
        tx, ty = tile_clicked
        for case in list(map.cases):
            if (case.entity is None):
                continue
            if (isinstance(case.entity, Bolgrot)
                    or isinstance(case.entity, Player)):
                continue
            dx = max(-1, min(1, tx - case.x))
            dy = max(-1, min(1, ty - case.y))
            if dx == 0 and dy == 0:
                continue
            target = self._find_case((case.x + dx, case.y + dy), map.cases)
            if target is not None and target.entity is None:
                target.entity = case.entity
                case.entity = None
        player.hp -= 5
        player.pa -= self.cost
        self.time_used += 1

    def next_turn(self):
        self.time_used = 0
