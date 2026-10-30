"""Shared trip, offer and action records used by the simulation.

Trips, commitments, stops, legs, plans and offers are immutable values. Move
and Operation are mutable because a taxi advances its current physical action.
Distances are in metres; estimated and observed times are in seconds unless
a field explicitly names ticks.
"""

from dataclasses import dataclass
from enum import Enum
from .city import Cell, Heading


class PassengerState(str, Enum):
    """Passenger lifecycle; only a completed descent counts as delivered."""
    FUTURE = "future"
    WAITING = "waiting"
    RESERVED = "reserved"
    BOARDING = "boarding"
    ONBOARD = "onboard"
    ALIGHTING = "alighting"
    DELIVERED = "delivered"


@dataclass(frozen=True)
class Trip:
    """One request with fixed direct distance and cumulative detour allowance."""
    passenger_id: int
    origin: Cell
    destination: Cell
    appearance_tick: int
    reference_m: float
    budget_m: float


@dataclass(frozen=True)
class Commitment:
    """Confirmed trip with a fixed spatial promise until its pickup."""
    trip: Trip
    confirmation_odometer_m: float
    approach_limit_m: float


@dataclass(frozen=True)
class Stop:
    """One pickup or drop at a building's fixed road access."""
    passenger_id: int
    pickup: bool
    cell: Cell


@dataclass(frozen=True)
class Leg:
    """Road cells still to traverse before serving a stop, excluding departure."""
    stop: Stop
    cells: tuple[Cell, ...]


@dataclass(frozen=True)
class Plan:
    """Hypothetical route plus the measurements used to compare its offer.

    distance_m includes any remaining portion already entered by the taxi.
    candidate_pickup_seconds is an absolute estimated time, before boarding.
    budget_score is the largest share of detour budget used by any affected
    passenger. Estimated times use free speed, not predicted congestion.
    """
    legs: tuple[Leg, ...]
    distance_m: float
    candidate_approach_m: float
    candidate_pickup_seconds: float
    candidate_ride_m: float
    budget_score: float


@dataclass(frozen=True)
class Offer:
    """One taxi's proposed plan for a passenger, valid for one message round."""
    passenger_id: int
    taxi_id: int
    round_id: int
    plan: Plan

    @property
    def identity(self):
        return self.passenger_id, self.taxi_id, self.round_id


@dataclass
class Move:
    """One directed road portion, locked until all CELL_METERS are travelled."""
    origin: Cell
    target: Cell
    heading: Heading
    progressed_m: float = 0.0


@dataclass
class Operation:
    """Boarding or alighting in progress, completed after its remaining ticks."""
    stop: Stop
    remaining_ticks: int
