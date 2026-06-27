import random as _random


class Patterns:
    _all_patterns: list[list[tuple[int, int]]] = [
        [(14, 11), (13, 8), (7, 9), (13, 22), (19, 21), (3, 12)],
        [(15, 10)],
    ]

    def __init__(self, seed: int | None = None) -> None:
        self._rng = _random.Random(seed)
        self.spawn_patterns: list[list[tuple[int, int]]] = list(self._all_patterns)

    def draw(self) -> list[tuple[int, int]]:
        if not self.spawn_patterns:
            return []
        pattern = self._rng.choice(self.spawn_patterns)
        self.spawn_patterns.remove(pattern)
        return pattern

    def reset(self) -> None:
        self.spawn_patterns = list(self._all_patterns)
