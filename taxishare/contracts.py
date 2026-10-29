"""Immutable values exchanged by agents and consumed by route planning."""

from dataclasses import dataclass
from enum import Enum
from .city import Cell, Heading


class PassengerState(str, Enum):
    FUTURE = "future"
    WAITING = "waiting"
    RESERVED = "reserved"
    BOARDING = "boarding"
    ONBOARD = "onboard"
    ALIGHTING = "alighting"
    DELIVERED = "delivered"


@dataclass(frozen=True)
class Trip:
    passenger_id: int
    origin: Cell
    destination: Cell
    appearance_tick: int
    reference_m: float
    budget_m: float


@dataclass(frozen=True)
class Commitment:
    trip: Trip
    confirmation_odometer_m: float
    approach_limit_m: float


@dataclass(frozen=True)
class Stop:
    passenger_id: int
    pickup: bool
    cell: Cell


@dataclass(frozen=True)
class Leg:
    stop: Stop
    cells: tuple[Cell, ...]


@dataclass(frozen=True)
class Plan:
    legs: tuple[Leg, ...]
    distance_m: float
    candidate_approach_m: float
    candidate_pickup_seconds: float
    candidate_ride_m: float
    budget_score: float


@dataclass(frozen=True)
class Offer:
    passenger_id: int
    taxi_id: int
    round_id: int
    plan: Plan

    @property
    def identity(self):
        return self.passenger_id, self.taxi_id, self.round_id


@dataclass
class Move:
    origin: Cell
    target: Cell
    heading: Heading
    progressed_m: float = 0.0


@dataclass
class Operation:
    stop: Stop
    remaining_ticks: int
