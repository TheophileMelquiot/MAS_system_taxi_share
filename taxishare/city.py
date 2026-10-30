"""Road geometry and deterministic shortest paths between road cells.

Each edge is one 100 m movement. U-turns are allowed at cell boundaries;
headings describe physical movement and display, not routing constraints.
"""

from collections import deque
from dataclasses import dataclass
from .config import CELL_METERS

Cell = tuple[int, int]
Heading = tuple[int, int]
DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


@dataclass(frozen=True)
class Building:
    building_id: int
    cell: Cell
    access: Cell


class City:
    """Finite bidirectional full axes with an outer road frame."""

    def __init__(self, width, height, horizontal, vertical, buildings=()):
        self.width, self.height = width, height
        self.horizontal = tuple(sorted(horizontal))
        self.vertical = tuple(sorted(vertical))
        self.roads = frozenset((x, y) for x in range(width) for y in range(height)
                               if x in self.vertical or y in self.horizontal)
        self.adjacent = {p: tuple(q for d in DIRECTIONS
                                 if (q := (p[0] + d[0], p[1] + d[1])) in self.roads)
                         for p in sorted(self.roads)}
        self.buildings = tuple(buildings)
        self._trees = {}
        self._paths = {}

    def headings(self, cell: Cell) -> tuple[Heading, ...]:
        """An initial heading must correspond to a physically possible arrival."""
        return tuple((cell[0] - p[0], cell[1] - p[1]) for p in self.adjacent[cell])

    def service_cell(self, cell: Cell) -> bool:
        return cell in self.roads and len(self.adjacent[cell]) < 3

    def possible_accesses(self, cell: Cell) -> tuple[Cell, ...]:
        return tuple(sorted(q for dx, dy in DIRECTIONS
                            if self.service_cell(q := (cell[0] + dx, cell[1] + dy))))

    def _tree(self, start: Cell):
        """Cache one BFS tree per departure cell for all destinations."""
        if start not in self.roads:
            raise ValueError(f"Invalid road cell: {start}")
        if start not in self._trees:
            parents = {start: None}
            queue = deque([start])
            while queue:
                current = queue.popleft()
                for nxt in self.adjacent[current]:
                    if nxt not in parents:
                        parents[nxt] = current
                        queue.append(nxt)
            self._trees[start] = parents
        return self._trees[start]

    def path_to(self, start: Cell, target: Cell):
        """Return one shortest path, excluding start, or None if unreachable.

        Stable neighbor order breaks ties. A visit at the current cell needs
        no movement; the taxi may freely choose its next departure direction.
        """
        if target not in self.roads:
            raise ValueError(f"Invalid road cell: {target}")
        key = (start, target)
        if key in self._paths:
            return self._paths[key]
        parents = self._tree(start)
        result = None
        if target in parents:
            path, node = [], target
            while node != start:
                path.append(node)
                node = parents[node]
            result = tuple(reversed(path))
        self._paths[key] = result
        return result

    def reference_distance(self, origin: Cell, destination: Cell) -> float:
        """Personal D0 is the shortest road distance, fixed once per trip."""
        path = self.path_to(origin, destination)
        if path is None:
            raise ValueError("Unreachable destination")
        return len(path) * CELL_METERS

    def validate_accessibility(self):
        """A connected bidirectional network reaches every valid access."""
        if not self.roads or any(not neighbors for neighbors in self.adjacent.values()):
            raise ValueError("Road network must allow movement from every cell")
        if len(self._tree(min(self.roads))) != len(self.roads):
            raise ValueError("Disconnected road network")
        if any(b.access not in self.roads for b in self.buildings):
            raise ValueError("Building access is outside the road network")
