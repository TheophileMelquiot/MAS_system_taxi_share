"""Generate, validate and persist all exogenous inputs before simulation."""

from dataclasses import dataclass, asdict
from hashlib import sha256
import json
from pathlib import Path
import random
from .config import Config
from .city import Building, City, Cell, Heading

SCENARIO_VERSION = 1


def integer_pair(value):
    """JSON coordinates must contain exactly two integers, never booleans."""
    return isinstance(value, tuple) and len(value) == 2 and all(type(v) is int for v in value)


@dataclass(frozen=True)
class TaxiInitial:
    taxi_id: int
    cell: Cell
    heading: Heading


@dataclass(frozen=True)
class Request:
    passenger_id: int
    origin_id: int
    destination_id: int
    appearance_tick: int


def random_stream(seed: int, name: str) -> random.Random:
    """Namespaced SHA-256 avoids Python's process-dependent built-in hash."""
    digest = sha256(f"taxishare-v1:{seed}:{name}".encode()).digest()
    return random.Random(int.from_bytes(digest, "big"))


def draw_axes(size: int, count: int, spacing: int, rng) -> tuple[int, ...]:
    """Uniformly sample legal axis combinations using a gap-removing bijection."""
    inner = count - 2
    upper = size - 1 - (count - 1) * (spacing - 1)
    compressed = sorted(rng.sample(range(1, upper), inner))
    return (0, *(v + (i + 1) * (spacing - 1) for i, v in enumerate(compressed)), size - 1)


@dataclass(frozen=True)
class Scenario:
    config: Config
    horizontal: tuple[int, ...]
    vertical: tuple[int, ...]
    buildings: tuple[Building, ...]
    fleet: tuple[TaxiInitial, ...]
    requests: tuple[Request, ...]

    def city(self) -> City:
        return City(self.config.width, self.config.height,
                    self.horizontal, self.vertical, self.buildings)

    def validate(self) -> City:
        """Validate loaded inputs as strictly as generated inputs."""
        c = self.config
        for axes, size, count in ((self.horizontal, c.height, c.horizontal_axes),
                                  (self.vertical, c.width, c.vertical_axes)):
            if (len(axes) != count or any(type(x) is not int for x in axes)
                    or tuple(sorted(set(axes))) != axes or axes[0] != 0 or axes[-1] != size - 1
                    or any(b - a < c.axis_spacing for a, b in zip(axes, axes[1:]))):
                raise ValueError("Invalid road axes or missing outer frame")
        city = self.city()
        if (len(self.buildings) != c.buildings or len(self.fleet) != c.taxis
                or len(self.requests) != c.requests):
            raise ValueError("Scenario counts disagree with configuration")
        for records, attr in ((self.buildings, "building_id"), (self.fleet, "taxi_id"),
                              (self.requests, "passenger_id")):
            ids = [getattr(r, attr) for r in records]
            if any(type(i) is not int or i < 0 for i in ids) or len(set(ids)) != len(ids):
                raise ValueError(f"Invalid or duplicate {attr}")
        if len({b.cell for b in self.buildings}) != len(self.buildings):
            raise ValueError("Buildings must occupy distinct cells")
        for b in self.buildings:
            if not integer_pair(b.cell) or not integer_pair(b.access):
                raise ValueError(f"Invalid building coordinates: {b}")
            x, y = b.cell
            if (type(x) is not int or type(y) is not int or not (0 <= x < c.width and 0 <= y < c.height)
                    or b.cell in city.roads or b.access not in city.possible_accesses(b.cell)):
                raise ValueError(f"Invalid building or access: {b}")
        if len({b.access for b in self.buildings}) < 2:
            raise ValueError("At least two distinct usable accesses are required")
        if len({t.cell for t in self.fleet}) != len(self.fleet):
            raise ValueError("Initial taxi positions must be distinct")
        for t in self.fleet:
            if (not integer_pair(t.cell) or not integer_pair(t.heading)
                    or not city.service_cell(t.cell) or t.heading not in city.headings(t.cell)):
                raise ValueError(f"Invalid initial taxi state: {t}")
        buildings = {b.building_id: b for b in self.buildings}
        for r in self.requests:
            if (type(r.origin_id) is not int or type(r.destination_id) is not int
                    or r.origin_id not in buildings or r.destination_id not in buildings
                    or buildings[r.origin_id].access == buildings[r.destination_id].access
                    or type(r.appearance_tick) is not int
                    or not 0 <= r.appearance_tick <= c.appearance_ticks):
                raise ValueError(f"Invalid request: {r}")
        city.validate_oriented_accessibility()
        return city

    def to_dict(self):
        return {"schema_version": SCENARIO_VERSION, **asdict(self)}

    @property
    def fingerprint(self):
        data = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
        return sha256(data.encode()).hexdigest()

    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path):
        """Reject legacy schemas explicitly; never reinterpret old business rules."""
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        if raw.get("schema_version") != SCENARIO_VERSION:
            raise ValueError("Unsupported scenario version; regenerate or explicitly migrate it")
        try:
            scenario = cls(
                Config(**raw["config"]), tuple(raw["horizontal"]), tuple(raw["vertical"]),
                tuple(Building(b["building_id"], tuple(b["cell"]), tuple(b["access"]))
                      for b in raw["buildings"]),
                tuple(TaxiInitial(t["taxi_id"], tuple(t["cell"]), tuple(t["heading"]))
                      for t in raw["fleet"]),
                tuple(Request(**r) for r in raw["requests"]))
            scenario.validate()
            return scenario
        except (KeyError, TypeError, IndexError) as exc:
            raise ValueError(f"Malformed scenario: {exc}") from exc


def generate(config: Config) -> Scenario:
    """Four streams isolate map, fleet, trips and arrival times."""
    map_rng, fleet_rng, trip_rng, time_rng = (
        random_stream(config.seed, name) for name in ("map", "fleet", "trips", "times"))
    horizontal = draw_axes(config.height, config.horizontal_axes, config.axis_spacing, map_rng)
    vertical = draw_axes(config.width, config.vertical_axes, config.axis_spacing, map_rng)
    city = City(config.width, config.height, horizontal, vertical)
    candidates = [(x, y) for x in range(config.width) for y in range(config.height)
                  if (x, y) not in city.roads and city.possible_accesses((x, y))]
    if len(candidates) < config.buildings:
        raise ValueError(f"Only {len(candidates)} admissible building cells")
    buildings = tuple(Building(i, cell, min(city.possible_accesses(cell)))
                      for i, cell in enumerate(map_rng.sample(candidates, config.buildings)))
    eligible = sorted(p for p in city.roads if city.service_cell(p))
    if config.taxis > len(eligible):
        raise ValueError(f"Only {len(eligible)} distinct initial taxi positions")
    positions = fleet_rng.sample(eligible, config.taxis)
    fleet = tuple(TaxiInitial(i, p, fleet_rng.choice(city.headings(p))) for i, p in enumerate(positions))
    destinations = {b.building_id: tuple(d.building_id for d in buildings if d.access != b.access)
                    for b in buildings}
    if not all(destinations.values()):
        raise ValueError("Buildings must expose at least two distinct accesses")
    requests = []
    for i in range(config.requests):
        origin = trip_rng.choice(buildings).building_id
        requests.append(Request(i, origin, trip_rng.choice(destinations[origin]),
                                time_rng.randint(0, config.appearance_ticks)))
    scenario = Scenario(config, horizontal, vertical, buildings, fleet, tuple(requests))
    scenario.validate()
    return scenario
