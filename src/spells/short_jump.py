from __future__ import annotations
from typing import TYPE_CHECKING
from .spells import Spells, TypeSpell

if TYPE_CHECKING:
    from ..entity import Player
    from ..map import Map


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

    def play(
        self,
        map: Map,
        player: Player,
        tile_clicked: tuple[int, int]
    ) -> None:
        if tile_clicked not in self.previsu(
                (player.pos_x, player.pos_y), map.cases):
            return
        src = self._find_case((player.pos_x, player.pos_y), map.cases)
        dst = self._find_case(tile_clicked, map.cases)
        if src is None or dst is None:
            return
        src.entity = None
        player.pos_x, player.pos_y = tile_clicked
        player.hp -= 1
        player.pa -= self.cost
        dst.entity = player
