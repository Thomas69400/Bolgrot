from ..map import Map
from ..case import CaseType


class BFS:
    def __init__(
        self,
        map: Map
    ):
        self.map: Map = map

    def find_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int]
    ) -> tuple[int, int] | None:
        """Find the shortest path from start to goal using BFS."""
        from collections import deque

        queue = deque([start])
        visited = {start: None}

        while queue:
            current = queue.popleft()

            if current == goal:
                path = []
                while current is not None:
                    path.append(current)
                    current = visited[current]
                path.pop(-1)
                return path[-1]

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)

        return None

    def get_neighbors(
        self,
        pos: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Get valid neighboring positions (up, down, left, right)."""
        x, y = pos
        neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]
        valid_neighbors = [
            (nx, ny) for nx, ny in neighbors
            if self.is_valid_position((nx, ny))
        ]
        return valid_neighbors

    def is_valid_position(
        self,
        pos: tuple[int, int]
    ) -> bool:
        """Check if the position is within the map and not blocked."""
        x, y = pos
        for case in self.map.cases:
            if (case.x, case.y) == (x, y):
                return case.case_type != CaseType.WALL
        return False
