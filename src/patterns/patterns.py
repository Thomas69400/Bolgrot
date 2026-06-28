import random as _random


class Patterns:
    """Pool of flame spawn patterns, drawn at random without replacement.

    Uses a seeded ``random.Random`` so a given seed yields a reproducible
    sequence of draws.
    """

    _all_patterns: list[list[tuple[int, int]]] = [
        [(14, 11), (13, 8), (7, 9), (13, 22), (19, 21), (3, 12)],
        [(15, 10)],
    ]

    def __init__(self, seed: int | None = None) -> None:
        """Seed the RNG and copy the full pattern pool into the draw pool."""
        self._rng = _random.Random(seed)
        self.spawn_patterns: list[list[tuple[int, int]]] = list(
            self._all_patterns)

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
