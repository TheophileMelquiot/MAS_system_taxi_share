"""Pure constrained insertion, with no mutations or reads of other agents.

For each pickup/drop insertion, search shortest legal paths for every arrival
heading. Existing stops keep their relative order. A locked move/operation is
accounted for before any change. This is not a global fleet optimizer.
"""

from dataclasses import dataclass
from .city import State
from .config import CELL_METERS, FREE_SPEED_MPS, EPSILON
from .contracts import Commitment, Leg, Plan, Stop, Trip


@dataclass(frozen=True)
class PlanningContext:
    anchor: State
    now_seconds: float
    prefix_distance_m: float
    locked_seconds: float
    odometer_m: float
    occupied: frozenset[int]
    ridden: dict[int, float]
    commitments: dict[int, Commitment]
    stops: tuple[Stop, ...]
    capacity: int


@dataclass
class Label:
    state: State
    distance_m: float
    seconds: float
    occupied: frozenset[int]
    ridden: dict[int, float]
    pickup_distances: dict[int, float]
    pickup_seconds: dict[int, float]
    legs: tuple[Leg, ...]


def plan_key(plan: Plan):
    """Taxi choice: distance first; ties use stops and then concrete paths."""
    return (round(plan.distance_m, 7),
            tuple((leg.stop.passenger_id, leg.stop.pickup, leg.cells) for leg in plan.legs))


class InsertionPlanner:
    def __init__(self, city):
        self.city = city

    def best_plan(self, context: PlanningContext, candidate: Trip, promised=None):
        """Return the minimum-distance admissible insertion or a diagnostic.

        On revalidation, the accepted offer supplies upper bounds: pickup time,
        announced approach, personal ride distance and budget score cannot get
        worse. A different internal insertion is allowed only within all these
        promises; otherwise the client retries next round.
        """
        trips = {pid: c.trip for pid, c in context.commitments.items()}
        trips[candidate.passenger_id] = candidate
        best = None
        pickup = Stop(candidate.passenger_id, True, candidate.origin)
        drop = Stop(candidate.passenger_id, False, candidate.destination)
        for first in range(len(context.stops) + 1):
            with_pickup = context.stops[:first] + (pickup,) + context.stops[first:]
            for last in range(first + 1, len(with_pickup) + 1):
                stops = with_pickup[:last] + (drop,) + with_pickup[last:]
                if not self._valid_stop_order(stops, context.occupied, context.capacity):
                    continue
                for plan in self._route(context, candidate, trips, stops, best, promised):
                    if best is None or plan_key(plan) < plan_key(best):
                        best = plan
        return best, None if best else "no_feasible_insertion_under_capacity_distance_orientation_and_promises"

    @staticmethod
    def _valid_stop_order(stops, initial, capacity):
        """Places are released after a full drop, before any following pickup."""
        occupied = set(initial)
        for index, stop in enumerate(stops):
            if (index and stop.cell == stops[index - 1].cell
                    and not stop.pickup and stops[index - 1].pickup):
                return False  # At one service visit, drops precede pickups.
            if stop.pickup:
                if stop.passenger_id in occupied or len(occupied) >= capacity:
                    return False
                occupied.add(stop.passenger_id)
            else:
                if stop.passenger_id not in occupied:
                    return False
                occupied.remove(stop.passenger_id)
        return not occupied

    def _route(self, context, candidate, trips, stops, best, promised):
        ridden = dict(context.ridden)
        for pid in context.occupied:
            ridden[pid] = ridden.get(pid, 0) + context.prefix_distance_m
        if any(ridden.get(pid, 0) > t.reference_m + t.budget_m + EPSILON for pid, t in trips.items()):
            return
        labels = [Label(context.anchor, context.prefix_distance_m, context.locked_seconds,
                        context.occupied, ridden, {}, {}, ())]
        for stop in stops:
            following = []
            for label in labels:
                for cells, heading in self.city.paths_to(label.state, stop.cell):
                    distance = len(cells) * CELL_METERS
                    if best and label.distance_m + distance > best.distance_m + EPSILON:
                        continue
                    advanced = self._visit(context, label, stop, cells, heading, trips)
                    if advanced is not None:
                        following.append(advanced)
            labels = self._prune(following)
            if not labels:
                return
        pid = candidate.passenger_id
        for label in labels:
            score = max((max(0.0, label.ridden.get(i, 0) - t.reference_m) / t.budget_m
                         if t.budget_m else 0.0) for i, t in trips.items())
            plan = Plan(label.legs, label.distance_m, label.pickup_distances[pid],
                        context.now_seconds + label.pickup_seconds[pid], label.ridden[pid], score)
            if promised is not None and (
                    plan.candidate_approach_m > promised.candidate_approach_m + EPSILON
                    or plan.candidate_pickup_seconds > promised.candidate_pickup_seconds + EPSILON
                    or plan.candidate_ride_m > promised.candidate_ride_m + EPSILON
                    or plan.budget_score > promised.budget_score + EPSILON):
                continue
            yield plan

    @staticmethod
    def _visit(context, label, stop, cells, heading, trips):
        distance = len(cells) * CELL_METERS
        total = label.distance_m + distance
        seconds = label.seconds + distance / FREE_SPEED_MPS
        ridden = dict(label.ridden)
        for pid in label.occupied:
            ridden[pid] = ridden.get(pid, 0) + distance
            trip = trips[pid]
            if ridden[pid] > trip.reference_m + trip.budget_m + EPSILON:
                return None
        pickup_distances, pickup_seconds = dict(label.pickup_distances), dict(label.pickup_seconds)
        occupied = set(label.occupied)
        pid = stop.passenger_id
        if stop.pickup:
            commitment = context.commitments.get(pid)
            if commitment:
                consumed = context.odometer_m - commitment.confirmation_odometer_m
                if consumed + total > commitment.approach_limit_m + EPSILON:
                    return None
            pickup_distances[pid], pickup_seconds[pid] = total, seconds
            occupied.add(pid)
        else:
            occupied.remove(pid)
        return Label((stop.cell, heading), total, seconds + 2.0, frozenset(occupied),
                     ridden, pickup_distances, pickup_seconds, label.legs + (Leg(stop, cells),))

    @staticmethod
    def _prune(labels):
        """Only merge exactly equal resource states; keep the stable path tie.

        A shorter taxi route can still increase one person's ride. Pruning on
        total distance alone would silently discard feasible future solutions.
        """
        kept = {}
        for label in labels:
            key = (label.state, label.distance_m, label.seconds,
                   tuple(sorted(label.ridden.items())), tuple(sorted(label.pickup_distances.items())),
                   tuple(sorted(label.pickup_seconds.items())))
            previous = kept.get(key)
            if previous is None or tuple(l.cells for l in label.legs) < tuple(l.cells for l in previous.legs):
                kept[key] = label
        return list(kept.values())
