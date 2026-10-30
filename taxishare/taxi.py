"""Taxi behavior is split into reception, planning, commitment and physics.

Each taxi owns its demand cache, offers, commitments and action. The model
activates these short behaviors; it never selects a taxi for a passenger.
"""

from dataclasses import replace
from mesa import Agent
from .config import CELL_METERS, EPSILON, FREE_SPEED_MPS, OPERATION_TICKS, STEP_SECONDS
from .contracts import Commitment, Move, Offer, Operation
from .messaging import Kind
from .planning import PlanningContext


class Taxi(Agent):
    def __init__(self, model, initial):
        super().__init__(model)
        self.taxi_id = initial.taxi_id
        self.address = ("taxi", self.taxi_id)
        self.heading = initial.heading
        self.known_requests = {}
        self.offers = {}
        # Commitments are future obligations; occupied contains physical seats
        # in use. Sequential reservations may therefore outnumber the capacity.
        self.commitments = {}
        self.occupied = set()
        self.ridden = {}
        self.legs = []
        self.action = None
        self.odometer_m = 0.0
        self.distances = [0.0] * (model.config.capacity + 1)
        self.moving_seconds = 0.0
        self.operation_seconds = 0.0
        self.idle_seconds = 0.0
        self.congestion_seconds = 0.0
        self.quantization_seconds = 0.0
        self.delivered_count = 0
        self.last_failures = {}
        self.model.grid.place_agent(self, initial.cell)

    def receive_requests(self):
        """Keep local copies of active calls; there is no shared demand board."""
        for message in self.model.bus.receive(self.address, {Kind.CFP, Kind.CLOSE}):
            if message.kind == Kind.CFP:
                trip = message.payload
                assert message.sender == ("passenger", trip.passenger_id)
                self.known_requests[trip.passenger_id] = trip
            else:
                pid = message.payload
                assert message.sender == ("passenger", pid)
                self.known_requests.pop(pid, None)
                self.last_failures.pop(pid, None)
                self.offers.pop(pid, None)

    def make_offers(self):
        """Reevaluate known active trips once per tick without sending new CFPs."""
        self.offers.clear()
        # Every offer in this phase uses the same taxi snapshot. No place is
        # reserved until an acceptance is revalidated against live commitments.
        context = self.planning_context()
        for pid, trip in sorted(self.known_requests.items()):
            if pid in self.commitments:
                continue
            plan, reason = self.model.planner.best_plan(context, trip)
            if plan is None:
                self.last_failures[pid] = reason
                continue
            self.last_failures.pop(pid, None)
            offer = Offer(pid, self.taxi_id, self.model.tick, plan)
            self.offers[pid] = offer
            self._send(pid, Kind.OFFER, offer)

    def process_acceptances(self):
        """Oldest first, with atomic revalidation/commit before the next reply."""
        messages = self.model.bus.receive(self.address, {Kind.ACCEPT})
        valid = []
        for message in messages:
            pid, taxi_id, round_id = message.payload
            offer = self.offers.get(pid)
            if (message.sender != ("passenger", pid) or taxi_id != self.taxi_id
                    or round_id != self.model.tick or offer is None
                    or offer.identity != message.payload):
                self._send(pid, Kind.REJECT, (message.payload, "expired_or_unknown_offer"))
            else:
                valid.append(offer)
        valid.sort(key=lambda offer: (self.known_requests[offer.passenger_id].appearance_tick,
                                      offer.passenger_id))
        # Commit immediately after each successful revalidation so the next
        # acceptance cannot claim capacity or distance budgets already consumed.
        for offer in valid:
            self._revalidate_and_commit(offer)

    def _revalidate_and_commit(self, offer):
        """Offers reserve no resources. Accepted promises are never worsened."""
        pid = offer.passenger_id
        if pid in self.commitments:
            self._send(pid, Kind.REJECT, (offer.identity, "already_committed"))
            return
        trip = self.known_requests[pid]
        plan, reason = self.model.planner.best_plan(self.planning_context(), trip, offer.plan)
        if plan is None:
            self.last_failures[pid] = reason
            self._send(pid, Kind.REJECT, (offer.identity, reason))
            return
        self.commitments[pid] = Commitment(trip, self.odometer_m, offer.plan.candidate_approach_m)
        self.ridden[pid] = 0.0
        self.legs = list(plan.legs)
        self._send(pid, Kind.CONFIRM, (offer.identity, None))

    def close_round(self):
        self.receive_requests()
        self.offers.clear()

    def planning_context(self):
        """Freeze the current physical action; only its future suffix can change."""
        anchor = self.pos
        prefix, seconds = 0.0, 0.0
        occupied = set(self.occupied)
        if isinstance(self.action, Move):
            anchor = self.action.target
            prefix = max(0.0, CELL_METERS - self.action.progressed_m)
            seconds = prefix / FREE_SPEED_MPS
        elif isinstance(self.action, Operation):
            seconds = self.action.remaining_ticks * STEP_SECONDS
            if not self.action.stop.pickup:
                # This is the projected state AFTER the locked descent ends.
                # The real seat remains occupied until _finish_operation runs.
                occupied.remove(self.action.stop.passenger_id)
        return PlanningContext(anchor, self.model.time_seconds, prefix, seconds,
                               self.odometer_m, frozenset(occupied), dict(self.ridden),
                               dict(self.commitments), tuple(leg.stop for leg in self.legs),
                               self.model.config.capacity)

    def finalize_action(self):
        """Only phase 1 finalizes actions due at this boundary, once."""
        if isinstance(self.action, Move) and self.action.progressed_m >= CELL_METERS - EPSILON:
            self.model.grid.move_agent(self, self.action.target)
            self.heading = self.action.heading
            self.action = None
        elif isinstance(self.action, Operation) and self.action.remaining_ticks == 0:
            self._finish_operation()

    def _finish_operation(self):
        stop = self.action.stop
        pid = stop.passenger_id
        if stop.pickup:
            self._send(pid, Kind.BOARD_END, None)
        else:
            # Notify with the final distance before removing local accounting.
            # The passenger will retain that value after the trip is complete.
            self._send(pid, Kind.DROP_END, self.ridden[pid])
            self.occupied.remove(pid)  # The seat is released only now.
            del self.ridden[pid]
            del self.commitments[pid]
            self.delivered_count += 1
        self.action = None

    def start_action(self):
        """Start one legal physical action, or preserve the current one."""
        if self.action is not None or not self.legs:
            return
        leg = self.legs[0]
        if leg.cells:
            self._start_move(leg)
        else:
            self.legs.pop(0)
            self._start_operation(leg.stop)

    def _start_move(self, leg):
        target = leg.cells[0]
        heading = (target[0] - self.pos[0], target[1] - self.pos[1])
        assert target in self.model.city.adjacent[self.pos], "Illegal road move"
        self.legs[0] = replace(leg, cells=leg.cells[1:])
        self.action = Move(self.pos, target, heading)

    def _start_operation(self, stop):
        assert self.pos == stop.cell and self.model.city.service_cell(self.pos), "Illegal service location"
        pid = stop.passenger_id
        if stop.pickup:
            assert pid not in self.occupied, "Duplicate boarding"
            assert len(self.occupied) < self.model.config.capacity, "No free seat at boarding start"
            commitment = self.commitments[pid]
            assert self.odometer_m - commitment.confirmation_odometer_m <= commitment.approach_limit_m + EPSILON, "Broken approach promise"
            self.occupied.add(pid)  # Boarding consumes a seat immediately.
            self._send(pid, Kind.BOARD_START, None)
        else:
            assert pid in self.occupied, "Cannot drop a passenger who is not onboard"
            self._send(pid, Kind.DROP_START, None)
        self.action = Operation(stop, OPERATION_TICKS)

    def advance_action(self, speeds):
        """Advance exactly 0.2 s using an immutable common traffic snapshot."""
        if isinstance(self.action, Move):
            self._advance_move(speeds[(self.action.origin, self.action.target)])
        elif isinstance(self.action, Operation):
            assert self.action.remaining_ticks > 0, "An operation must be finalized before another interval"
            self.action.remaining_ticks -= 1
            self.operation_seconds += STEP_SECONDS
        else:
            assert not self.commitments, "A committed taxi must have an action or pending route"
            self.idle_seconds += STEP_SECONDS

    def _advance_move(self, speed):
        remaining = max(0.0, CELL_METERS - self.action.progressed_m)
        distance = min(remaining, speed * STEP_SECONDS)
        active_seconds = distance / speed
        self.action.progressed_m = min(CELL_METERS, self.action.progressed_m + distance)
        self.odometer_m += distance
        self.distances[len(self.occupied)] += distance
        for pid in self.occupied:
            self.ridden[pid] += distance
        self.moving_seconds += STEP_SECONDS
        # The whole tick belongs to circulation, but only distance/speed is
        # physical travel. Any unused tick fraction is quantization, not traffic.
        self.congestion_seconds += max(0.0, active_seconds - distance / FREE_SPEED_MPS)
        self.quantization_seconds += max(0.0, STEP_SECONDS - active_seconds)

    @property
    def status(self):
        if isinstance(self.action, Move):
            return "occupied" if self.occupied else "approach"
        if isinstance(self.action, Operation):
            return "boarding" if self.action.stop.pickup else "alighting"
        return "reserved" if self.commitments else "idle"

    def _send(self, passenger_id, kind, payload):
        self.model.bus.send(self.address, ("passenger", passenger_id), kind, self.model.tick, payload)
