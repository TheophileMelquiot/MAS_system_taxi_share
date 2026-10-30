"""Evaluate constrained insertions on a copied taxi snapshot.

For each pickup/drop insertion, follow one shortest path between each stop.
Existing stops keep their relative order. A locked move/operation is accounted
for before any change. City may cache paths, but no agent state is changed or
read here. The search selects one taxi's plan, not a global fleet assignment.
"""

from dataclasses import dataclass
from .city import Cell
from .config import CELL_METERS, FREE_SPEED_MPS, EPSILON, OPERATION_TICKS, STEP_SECONDS
from .contracts import Commitment, Leg, Plan, Stop, Trip


@dataclass(frozen=True)
class PlanningContext:
    """Taxi snapshot used for hypothetical plans, never the live taxi state.

    The anchor is the cell reached after the action already in progress.
    Its remaining distance and duration are carried by prefix_distance_m and
    locked_seconds. Existing commitments retain their original promises.
    """
    anchor: Cell
    now_seconds: float
    prefix_distance_m: float
    locked_seconds: float
    odometer_m: float
    occupied: frozenset[int]
    ridden: dict[int, float]
    commitments: dict[int, Commitment]
    stops: tuple[Stop, ...]
    capacity: int


def plan_key(plan: Plan):
    """Taxi choice: distance first; ties use stops and then concrete paths."""
    return (round(plan.distance_m, 7),
            tuple((leg.stop.passenger_id, leg.stop.pickup, leg.cells) for leg in plan.legs))


class InsertionPlanner:
    """Choose the shortest feasible insertion, with deterministic tie-breaking."""
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
        # Try only the new pickup/drop positions. Existing stops never change
        # their relative order, which bounds the search and preserves commitments.
        for first in range(len(context.stops) + 1):
            with_pickup = context.stops[:first] + (pickup,) + context.stops[first:]
            for last in range(first + 1, len(with_pickup) + 1):
                stops = with_pickup[:last] + (drop,) + with_pickup[last:]
                if not self._valid_stop_order(stops, context.occupied, context.capacity):
                    continue
                # Capacity is checked before routing because an impossible stop
                # order stays impossible regardless of the paths between stops.
                plan = self._route(context, candidate, trips, stops, best, promised)
                if plan is not None and (best is None or plan_key(plan) < plan_key(best)):
                    best = plan
        return best, None if best else "no_feasible_insertion_under_capacity_distance_and_promises"

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
        """Evaluate one stop order, or return None when a bound is exceeded.

        Distances belong to different accounts: total is taxi travel, ridden
        is per passenger, and pickup_distances protects each pending approach.
        All start from the same snapshot, so rejected trials have no effects.
        """
        ridden = dict(context.ridden)
        # Replanning cannot erase the rest of a road portion already entered.
        # Everyone currently aboard travels this prefix before any new stop.
        for pid in context.occupied:
            ridden[pid] = ridden.get(pid, 0) + context.prefix_distance_m
        if any(ridden.get(pid, 0) > t.reference_m + t.budget_m + EPSILON for pid, t in trips.items()):
            return
        cell = context.anchor
        total, seconds = context.prefix_distance_m, context.locked_seconds
        occupied = set(context.occupied)
        pickup_distances, pickup_seconds = {}, {}
        legs = []
        # With free U-turns, arrival direction cannot affect the next leg.
        # With free-speed ETA and distance caps, shortest legs minimize every
        # upper-bound resource. Predicted traffic or turn costs are not used.
        for stop in stops:
            cells = self.city.path_to(cell, stop.cell)
            if cells is None:
                return None
            distance = len(cells) * CELL_METERS
            total += distance
            seconds += distance / FREE_SPEED_MPS
            if best is not None and total > best.distance_m + EPSILON:
                # Later legs cannot reduce distance; this order cannot win.
                return None
            for pid in occupied:
                # Preserve distance already ridden, including the locked prefix.
                ridden[pid] = ridden.get(pid, 0) + distance
                trip = trips[pid]
                if ridden[pid] > trip.reference_m + trip.budget_m + EPSILON:
                    return None
            pid = stop.passenger_id
            if stop.pickup:
                commitment = context.commitments.get(pid)
                if commitment:
                    # Approach protection starts at the original confirmation.
                    consumed = context.odometer_m - commitment.confirmation_odometer_m
                    if consumed + total > commitment.approach_limit_m + EPSILON:
                        return None
                pickup_distances[pid], pickup_seconds[pid] = total, seconds
                occupied.add(pid)
            else:
                occupied.remove(pid)
            legs.append(Leg(stop, cells))
            # Every service takes time even when consecutive stops share a cell.
            seconds += OPERATION_TICKS * STEP_SECONDS
            cell = stop.cell
        pid = candidate.passenger_id
        # A zero budget permits no positive detour, already checked above.
        score = max((max(0.0, ridden.get(i, 0) - t.reference_m) / t.budget_m
                     if t.budget_m else 0.0) for i, t in trips.items())
        plan = Plan(tuple(legs), total, pickup_distances[pid],
                    context.now_seconds + pickup_seconds[pid], ridden[pid], score)
        if promised is not None and (
                plan.candidate_approach_m > promised.candidate_approach_m + EPSILON
                or plan.candidate_pickup_seconds > promised.candidate_pickup_seconds + EPSILON
                or plan.candidate_ride_m > promised.candidate_ride_m + EPSILON
                or plan.budget_score > promised.budget_score + EPSILON):
            # Revalidation may choose another insertion within the same promises.
            return None
        return plan
