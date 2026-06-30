from __future__ import annotations
from . import constant
from .BFS import BFS
from .map import Map
from .patterns import Patterns
from .spells import Spells, ShortJump, LongJump, MoveFlames
from .entity import Flame, Player, Bolgrot


class Game:
    """Owns all game state and the turn/action API (no pygame dependency)."""

    def __init__(
        self,
        player: Player,
        seed: int | None = None,
    ) -> None:
        """Set up the map, player spells, boss, spawn pattern and counters.

        ``seed`` makes the flame spawn sequence reproducible.
        """
        self.map: Map = Map()
        self.player: Player = player
        bfs: BFS = BFS(self.map)
        self.player.spells = [
            ShortJump(bfs=bfs),
            LongJump(bfs=bfs),
            MoveFlames(bfs=bfs),
        ]
        self.map.place_entity([constant.BASE_PLAYER_POS], self.player)
        self.map.place_entity([constant.BASE_BOLGROT_POS],
                              Bolgrot(*constant.BASE_BOLGROT_POS))
        self.patterns: Patterns = Patterns(seed=seed)
        self.spawn_pattern: list[tuple[int, int]] = \
            self.patterns.draw_opening()
        self.waves_spawned: int = 0
        self.previsualiation: list[tuple[int, int]] = []
        self.spell: Spells | None = None
        self.turn: int = 0
        self.done: bool = False
        self.won: bool = False

    def reset(self, seed: int | None = None) -> None:
        """Re-initialise all game state, optionally with a new seed."""
        self.__init__(self.player, seed=seed)  # type: ignore[misc]

    def select_spell(self, spell_index: int) -> None:
        """Select a spell and compute its previsualisation tiles.

        Does nothing for an out-of-range index; clears the previsualisation
        if the spell is not castable (not enough AP or uses exhausted).
        """
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
        if self.spell is None:
            return
        self.spell.play(self.map, self.player, tile_clicked)
        self.clear_previsu()
        self._check_end()

    def clear_previsu(self) -> None:
        """Discard the current previsualisation tiles."""
        self.previsualiation = []

    def end_turn(self) -> None:
        """Advance one turn: refresh AP/spells and spawn the next wave.

        Exactly ``constant.NB_WAVES`` distinct waves spawn over a game (one per
        end-turn until the quota is reached, none after). Once every wave has
        spawned, clearing all flames from the map wins the game.
        """
        self.player.pa = self.player.base_PA
        for spell in self.player.spells:
            spell.next_turn()
        if self.spawn_pattern:
            for pos in self.spawn_pattern:
                self.map.place_entity([pos], Flame(pos[0], pos[1]))
            self.waves_spawned += 1
            self.turn += 1
            self.spawn_pattern = (
                self.patterns.draw(self._occupied_tiles())
                if self.waves_spawned < constant.NB_WAVES
                else []
            )
        if self.waves_spawned >= 6:
            self.player.hp -= 1
        self.clear_previsu()
        self._check_end()

    def _occupied_tiles(self) -> set[tuple[int, int]]:
        """Tiles currently holding a flame or the player."""
        return {
            pos for pos, case in self.map.cases.items()
            if isinstance(case.entity, (Flame, Player))
        }

    def _flames_remain(self) -> bool:
        """Whether any flame is still on the map."""
        return any(isinstance(case.entity, Flame)
                   for case in self.map.cases.values())

    def _check_end(self) -> None:
        """Resolve win/loss: dead player loses; all waves cleared wins."""
        if self.player.hp <= 0:
            self.done = True
        elif self.waves_spawned >= constant.NB_WAVES and \
                not self._flames_remain():
            self.done = True
            self.won = True

    # def get_observation(self) -> dict:
    #     """Return a plain-dict snapshot of game state for a neural network.
    #     """
    #     flames = [pos for pos, v in self.map.cases.items()
    # if isinstance(v, Flame)]
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
    #     action: (spell_index, target_tile) to cast a spell, or None to end
    #     the turn.
    #     Reward is a placeholder (turns survived); replace with real fitness
    #     logic later.
    #     """
    #     if action is None:
    #         self.end_turn()
    #     else:
    #         spell_index, _target = action
    #         self.select_spell(spell_index)
    #     return float(self.turn), self.done
