import json as _json
import random as _random
from itertools import combinations as _combinations

from ..constant import PATTERNS_CONF


class Patterns:
    """Pool of flame spawn patterns, drawn at random without replacement.

    A pattern is the union of two "atoms" — fixed 3-tile constellations — drawn
    from a vocabulary loaded from ``patterns.json``. The two atoms must not both
    belong to the ``east`` region (those four atoms overlap spatially and never
    co-occur in the observed game), which is why only 114 of the C(16, 2) = 120
    atom pairs are legal.

    Uses a seeded ``random.Random`` so a given seed yields a reproducible
    sequence of draws.
    """

    _atoms: list[list[tuple[int, int]]] = []
    _all_patterns: list[list[tuple[int, int]]] = []
    _openings: list[list[tuple[int, int]]] = []

    @classmethod
    def _load(cls) -> None:
        """Load atoms from JSON and build the legal pattern pool once."""
        if cls._all_patterns:
            return
        with open(PATTERNS_CONF) as f:
            data = _json.load(f)
        cls._atoms = [[tuple(p) for p in atom] for atom in data["atoms"]]
        east = set(data["regions"]["east"])
        cls._all_patterns = [
            cls._atoms[i] + cls._atoms[j]
            for i, j in _combinations(range(len(cls._atoms)), 2)
            if not (i in east and j in east)
        ]
        # Fixed set of opening waves (the first wave is always one of these).
        cls._openings = [
            cls._atoms[i] + cls._atoms[j] for i, j in data["openings"]
        ]

    def __init__(self, seed: int | None = None) -> None:
        """Seed the RNG and copy the full pattern pool into the draw pool."""
        self._load()
        self._rng = _random.Random(seed)
        self.spawn_patterns: list[list[tuple[int, int]]] = list(
            self._all_patterns)

    def draw_opening(self) -> list[tuple[int, int]]:
        """Draw the first wave from the fixed opening set (without repeat)."""
        pattern = self._rng.choice(self._openings)
        if pattern in self.spawn_patterns:
            self.spawn_patterns.remove(pattern)
        return pattern

    def draw(self) -> list[tuple[int, int]]:
        """Pick and remove a random pattern; return ``[]`` when exhausted."""
        if not self.spawn_patterns:
            return []
        pattern = self._rng.choice(self.spawn_patterns)
        self.spawn_patterns.remove(pattern)
        return pattern

    def reset(self) -> None:
        """Restore the draw pool to the full set of patterns."""
        self.spawn_patterns = list(self._all_patterns)
