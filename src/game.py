from __future__ import annotations
from . import constant
from .BFS import BFS
from .map import Map
from .patterns import Patterns
from .spells import Spells
from .entity import Flame, Player, Entity, Bolgrot


class Game:
    def __init__(
        self,
        player: Player,
        seed: int | None = None,
    ) -> None:
        self.map: Map = Map()
        self.player: Player = player
        for spell in self.player.spells:
            spell.BFS = BFS(self.map)
        self.map.place_entity([constant.BASE_PLAYER_POS], self.player)
        self.map.place_entity([constant.BASE_BOLGROT_POS],
                              Bolgrot(*constant.BASE_BOLGROT_POS))
        self.patterns: Patterns = Patterns(seed=seed)
        self.spawn_pattern: list[tuple[int, int]] = self.patterns.draw()
        self.previsualiation: list[tuple[int, int]] = []
        self.spell: Spells | None = None
        self.turn: int = 0
        self.done: bool = False

    def reset(self, seed: int | None = None) -> None:
        self.__init__(seed=seed)

    def select_spell(self, spell_index: int) -> None:
        """Compute previsu for the spell. Sets self.previsualiation."""
        if spell_index < 0 or spell_index >= len(self.player.spells):
            return
        spell: Spells = self.player.spells[spell_index]
        if not spell.is_castable(self.player):
            self.clear_previsu()
            return
        self.spell = spell
        self.previsualiation = spell.previsu(
            (self.player.pos_x, self.player.pos_y), self.map.cases)

    def play_selected_spell(
            self,
            tile_clicked: tuple[int, int] | None = None,
    ) -> None:
        """Play the selected spell on the clicked tile, if valid."""
        if not self.previsualiation or tile_clicked is None:
            return

        self.spell.play(self.map, self.player, tile_clicked)
        self.clear_previsu()

    def clear_previsu(self) -> None:
        self.previsualiation = []

    def end_turn(self) -> None:
        self.player.hp -= 1
        self.player.pa = self.player.base_PA
        for spell in self.player.spells:
            spell.next_turn()
        if len(self.spawn_pattern) == 0:
            return
        for pos in self.spawn_pattern:
            self.map.place_entity([pos], Flame(pos[0], pos[1]))
        self.spawn_pattern = self.patterns.draw()
        self.previsualiation = []
        self.turn += 1

    # def get_observation(self) -> dict:
    #     """Return a plain-dict snapshot of game state for a neural network."""
    #     flames = [pos for pos, v in self.map.cases.items() if isinstance(v, Flame)]
    #     return {
    #         "player_pos": (self.player.pos_x, self.player.pos_y),
    #         "player_hp": self.player.hp,
    #         "player_ap": self.player.base_PA,
    #         "bolgrot_pos": (self.map.bolgrot.pos_x, self.map.bolgrot.pos_y),
    #         "flames": flames,
    #         "next_spawn": self.spawn_pattern,
    #         "turn": self.turn,
    #     }

    # def step(
    #     self,
    #     action: tuple[int, tuple[int, int]] | None,
    # ) -> tuple[float, bool]:
    #     """
    #     Apply one action and return (reward, done).
    #     action: (spell_index, target_tile) to cast a spell, or None to end the turn.
    #     Reward is a placeholder (turns survived); replace with real fitness logic later.
    #     """
    #     if action is None:
    #         self.end_turn()
    #     else:
    #         spell_index, _target = action
    #         self.select_spell(spell_index)
    #     return float(self.turn), self.done
