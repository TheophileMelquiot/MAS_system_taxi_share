"""Road geometry and deterministic routing in (position, incoming heading).

A heading records how a taxi arrived, even while parked. Each graph edge is
one 100 m movement. Searching this graph prevents illegal hidden U-turns.
"""

from collections import deque
from dataclasses import dataclass
from .config import CELL_METERS

Cell = tuple[int, int]
Heading = tuple[int, int]
State = tuple[Cell, Heading]
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

    def successors(self, state: State) -> tuple[State, ...]:
        cell, heading = state
        return tuple((q, (q[0] - cell[0], q[1] - cell[1]))
                     for q in self.adjacent[cell]
                     if (q[0] - cell[0], q[1] - cell[1]) != (-heading[0], -heading[1]))

    def service_cell(self, cell: Cell) -> bool:
        return cell in self.roads and len(self.adjacent[cell]) < 3

    def possible_accesses(self, cell: Cell) -> tuple[Cell, ...]:
        return tuple(sorted(q for dx, dy in DIRECTIONS
                            if self.service_cell(q := (cell[0] + dx, cell[1] + dy))))

    def paths_to(self, start: State, target: Cell):
        """Return one shortest legal path per reachable final orientation.

        A nonzero loop back to an access is useful when an opposite arrival
        orientation is required. Zero distance is available only at the current
        orientation; stopping does not reset the heading.
        """
        key = (start, target)
        if key in self._paths:
            return self._paths[key]
        if start not in self._trees:
            if start[0] not in self.roads or start[1] not in self.headings(start[0]):
                raise ValueError(f"Invalid oriented road state: {start}")
            # Each edge is 100 m, so breadth-first search minimizes distance.
            # One tree serves every destination queried from this oriented start.
            parents = {start: None}
            queue = deque([start])
            while queue:
                current = queue.popleft()
                for nxt in self.successors(current):
                    if nxt not in parents:
                        parents[nxt] = current
                        queue.append(nxt)
            self._trees[start] = parents
        parents = self._trees[start]
        choices = []
        # Keep one path per arrival heading: the shortest arrival at this stop
        # may face the wrong way for the passenger's next leg.
        for heading in self.headings(target):
            end = (target, heading)
            if end not in parents:
                continue
            path, node = [], end
            while node != start:
                path.append(node[0])
                node = parents[node]
            choices.append((tuple(reversed(path)), heading))
        result = tuple(sorted(choices, key=lambda item: (len(item[0]), item[0], item[1])))
        self._paths[key] = result
        return result

    def reference_distance(self, origin: Cell, destination: Cell) -> float:
        """Personal D0 uses the best possible departure heading, once per trip."""
        lengths = [len(path) for h in self.headings(origin)
                   for path, _ in self.paths_to((origin, h), destination)]
        if not lengths:
            raise ValueError("Unreachable destination")
        return min(lengths) * CELL_METERS

    def validate_oriented_accessibility(self):
        """Reverse reachability proves every legal state can reach every access.

        This checks access positions, not every possible arrival heading. It
        also rejects states without any legal continuation after a stop.
        """
        states = {(p, h) for p in self.roads for h in self.headings(p)}
        reverse = {s: [] for s in states}
        for state in sorted(states):
            following = self.successors(state)
            if not following:
                raise ValueError(f"No legal continuation from {state}")
            for nxt in following:
                reverse[nxt].append(state)
        for access in sorted({b.access for b in self.buildings}):
            # Search backwards from all legal arrivals at this access. Seeing
            # every road state proves every taxi orientation can reach it.
            seen = {(access, h) for h in self.headings(access)}
            queue = deque(sorted(seen))
            while queue:
                for previous in reverse[queue.popleft()]:
                    if previous not in seen:
                        seen.add(previous)
                        queue.append(previous)
            if seen != states:
                raise ValueError(f"Access {access} unreachable from {min(states - seen)}")
