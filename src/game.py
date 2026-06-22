from __future__ import annotations
from .map import Map
from .patterns import Patterns
from .entity import Flame
from .spells import Spells


class Game:
    def __init__(self, seed: int | None = None) -> None:
        self.map: Map = Map()
        self.player = self.map.player
        self.patterns: Patterns = Patterns(seed=seed)
        self.spawn_pattern: list[tuple[int, int]] = self.patterns.draw()
        self.previsualiation: list[tuple[int, int]] = []
        self.turn: int = 0
        self.done: bool = False

    def reset(self, seed: int | None = None) -> None:
        self.__init__(seed=seed)

    def select_spell(self, spell_index: int) -> None:
        """Compute previsu for the spell. Sets self.previsualiation."""
        if spell_index < 0 or spell_index >= len(self.player.spells):
            return
        spell: Spells = self.player.spells[spell_index]
        self.previsualiation = spell.previsu(
            (self.player.pos_x, self.player.pos_y), self.map.cases)
        if self.previsualiation:
            spell.play()

    def clear_previsu(self) -> None:
        self.previsualiation = []

    def end_turn(self) -> None:
        self.map.place_flames(self.spawn_pattern)
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
