"""Central configuration and physical constants (SI units).

Business rules are deliberately not configurable switches. In particular,
U-turns are allowed at cell boundaries without an added maneuver duration.
Passenger transfers, abandonment and polling delays are not options.
"""

from dataclasses import dataclass, asdict
import math

STEP_SECONDS = 0.2
CELL_METERS = 100.0
# 50 km/h = 125/9 m/s: a free road portion takes exactly 36 ticks (7.2 s).
# Boarding and alighting each occupy ten whole ticks (2 s).
FREE_SPEED_MPS = 125 / 9
OPERATION_TICKS = 10
EPSILON = 1e-7  # Numerical tolerance, never an extra detour allowance.


@dataclass(frozen=True)
class Config:
    width: int = 21
    height: int = 21
    horizontal_axes: int = 5
    vertical_axes: int = 5
    axis_spacing: int = 2
    buildings: int = 32
    taxis: int = 8
    requests: int = 60
    appearance_seconds: float = 300.0
    capacity: int = 3
    congestion_threshold: float = 2.0
    detour_rate: float = 0.25
    detour_cap_m: float = 400.0
    seed: int = 2026
    max_seconds: float = 7200.0

    def __post_init__(self):
        """Reject impossible inputs instead of silently changing the scenario."""
        for name in ("width", "height", "horizontal_axes", "vertical_axes",
                     "axis_spacing", "buildings", "taxis", "requests", "capacity", "seed"):
            value = getattr(self, name)
            if type(value) is not int:
                raise ValueError(f"{name} must be an integer")
        if self.seed < 0 or self.requests < 0 or self.taxis < 1:
            raise ValueError("Require seed >= 0, requests >= 0 and taxis >= 1")
        if self.buildings < 2 or not 1 <= self.capacity <= 4:
            raise ValueError("Require at least two buildings and capacity in [1, 4]")
        if self.axis_spacing < 2:
            raise ValueError("Parallel road axes must be at least two cells apart")
        for size, count in ((self.width, self.vertical_axes),
                            (self.height, self.horizontal_axes)):
            if count < 2 or size < 3 or (count - 1) * self.axis_spacing > size - 1:
                raise ValueError("Map dimensions cannot accommodate the requested axes")
        for name in ("appearance_seconds", "congestion_threshold", "detour_rate",
                     "detour_cap_m", "max_seconds"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
            if value < 0:
                raise ValueError(f"{name} cannot be negative")
        if self.congestion_threshold <= 0 or self.max_seconds <= 0:
            raise ValueError("Congestion threshold and time limit must be positive")
        for name in ("appearance_seconds", "max_seconds"):
            ticks = getattr(self, name) / STEP_SECONDS
            if abs(ticks - round(ticks)) > EPSILON:
                raise ValueError(f"{name} must be a multiple of {STEP_SECONDS} s")

    @property
    def appearance_ticks(self):
        return round(self.appearance_seconds / STEP_SECONDS)

    @property
    def max_ticks(self):
        return round(self.max_seconds / STEP_SECONDS)

    def budget(self, reference_m: float) -> float:
        """Limit extra distance both proportionally to D0 and in absolute metres.

        This allowance applies cumulatively over the whole passenger journey;
        it is not renewed after each insertion or road portion.
        """
        return min(self.detour_rate * reference_m, self.detour_cap_m)

    def to_dict(self):
        return asdict(self)
