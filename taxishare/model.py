"""Mesa model coordinating a common clock, not making agent decisions."""

from collections import defaultdict
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from .config import EPSILON, STEP_SECONDS, FREE_SPEED_MPS
from .contracts import PassengerState, Trip
from .messaging import MessageBus
from .passenger import Passenger
from .taxi import Taxi
from .planning import InsertionPlanner
from .traffic import traffic_snapshot


class TaxiShareModel(Model):
    """One round per tick. Physical actions remain independent across taxis.

    Mesa's own step counter counts calls; `tick` is the explicit physical
    boundary counter, including the initial boundary at t=0.
    """

    def __init__(self, scenario, *, trace_messages=False, check_invariants=True):
        super().__init__(seed=scenario.config.seed)
        self.scenario = scenario
        self.config = scenario.config
        self.city = scenario.validate()
        self.grid = MultiGrid(self.config.width, self.config.height, torus=False)
        self.planner = InsertionPlanner(self.city)
        self.bus = MessageBus(trace_messages)
        self.tick = 0
        self.status = "running"
        self.stop_reason = None
        self.check_invariants = check_invariants
        self.loads, self.speeds = {}, {}
        self.taxis = [Taxi(self, initial) for initial in sorted(scenario.fleet, key=lambda t: t.taxi_id)]
        self.taxi_addresses = tuple(t.address for t in self.taxis)
        buildings = {b.building_id: b for b in scenario.buildings}
        self.passengers = []
        self._appearances = defaultdict(list)
        for request in sorted(scenario.requests, key=lambda r: r.passenger_id):
            origin = buildings[request.origin_id].access
            destination = buildings[request.destination_id].access
            reference = self.city.reference_distance(origin, destination)
            trip = Trip(request.passenger_id, origin, destination, request.appearance_tick,
                        reference, self.config.budget(reference))
            passenger = Passenger(self, trip)
            self.passengers.append(passenger)
            self._appearances[request.appearance_tick].append(passenger)
        self.data = DataCollector(model_reporters={
            "time_seconds": "time_seconds",
            "delivered": lambda m: sum(p.state == PassengerState.DELIVERED for p in m.passengers),
            "waiting": lambda m: sum(p.state == PassengerState.WAITING for p in m.passengers),
            "reserved": lambda m: sum(p.state == PassengerState.RESERVED for p in m.passengers),
            "distance_m": lambda m: sum(t.odometer_m for t in m.taxis),
            "shared_distance_m": lambda m: sum(sum(t.distances[2:]) for t in m.taxis),
            "empty_distance_m": lambda m: sum(t.distances[0] for t in m.taxis),
            "congestion_vehicle_seconds": lambda m: sum(t.congestion_seconds for t in m.taxis),
            "quantization_vehicle_seconds": lambda m: sum(t.quantization_seconds for t in m.taxis),
        })
        self.datacollector = self.data

    @property
    def time_seconds(self):
        return self.tick * STEP_SECONDS

    def _activate(self, agent_type, behavior, *args):
        """Use Mesa AgentSet activation while preserving the prescribed phases."""
        group = self.agents_by_type.get(agent_type)
        if group is not None:
            group.do(behavior, *args)

    def step(self):
        """Execute the nine specified phases without wall-clock sleeps."""
        if not self.running:
            return
        self._finalize_boundary()                         # 1. Complete due actions.
        self._release_requests()                          # 2. Reveal due calls.
        if self._check_completion_or_limit():
            self._observe()
            return
        self._negotiate()                                 # 3-6. One message round.
        if self._check_frozen_state():
            self._observe()
            return
        self._activate(Taxi, "start_action")               # 7. Preserve/start actions.
        self._activate(Passenger, "receive_transport")
        self.loads, self.speeds = traffic_snapshot(         # 8. Common loads.
            self.taxis, self.config.congestion_threshold)
        self._observe()
        self._activate(Taxi, "advance_action", self.speeds) # 9. Advance one interval.
        self.tick += 1
        if self.check_invariants:
            self.assert_invariants()

    def _finalize_boundary(self):
        self._activate(Taxi, "finalize_action")
        self._activate(Passenger, "receive_transport")

    def _release_requests(self):
        for passenger in self._appearances.pop(self.tick, ()):
            passenger.announce()

    def _negotiate(self):
        self._activate(Taxi, "receive_requests")
        self._activate(Taxi, "make_offers")
        self._round_offer_count = sum(len(t.offers) for t in self.taxis)
        self._activate(Passenger, "choose_offer")
        self._activate(Taxi, "process_acceptances")
        self._activate(Passenger, "receive_decision")
        self._activate(Taxi, "close_round")

    def _check_completion_or_limit(self):
        if all(p.state == PassengerState.DELIVERED for p in self.passengers):
            self._stop("complete", "all_passengers_delivered")
        elif self.tick >= self.config.max_ticks:
            self._stop("incomplete", "time_limit")
        return not self.running

    def _check_frozen_state(self):
        future = bool(self._appearances)
        parked = all(t.action is None and not t.commitments and not t.legs for t in self.taxis)
        waiting = any(p.state == PassengerState.WAITING for p in self.passengers)
        if not future and parked and waiting and self._round_offer_count == 0:
            self._stop("incomplete", "frozen_no_feasible_offer")
        return not self.running

    def _stop(self, status, reason):
        self.running = False
        self.status, self.stop_reason = status, reason

    def _observe(self):
        if self.check_invariants:
            self.assert_invariants()
        self.data.collect(self)

    def run_to_end(self):
        while self.running:
            self.step()
        return self

    def assert_invariants(self):
        """Global observation is permitted for checks, never agent decisions."""
        assignments = {}
        for taxi in self.taxis:
            assert taxi.pos in self.city.roads, "Taxi left the road network"
            assert taxi.heading in self.city.headings(taxi.pos), "Impossible incoming heading"
            assert len(taxi.occupied) <= self.config.capacity, "Physical capacity exceeded"
            assert taxi.occupied <= taxi.commitments.keys(), "Occupant without commitment"
            assert abs(sum(taxi.distances) - taxi.odometer_m) < 1e-5, "Distance counted twice or lost"
            total_time = taxi.moving_seconds + taxi.operation_seconds + taxi.idle_seconds
            assert abs(total_time - self.time_seconds) < 1e-5, "Physical action progressed twice"
            decomposed = taxi.odometer_m / FREE_SPEED_MPS + taxi.congestion_seconds + taxi.quantization_seconds
            assert abs(decomposed - taxi.moving_seconds) < 1e-5, "Congestion/quantization accounting mismatch"
            for pid, commitment in taxi.commitments.items():
                assert pid not in assignments, "Passenger assigned to multiple taxis"
                assignments[pid] = taxi
                trip = commitment.trip
                assert taxi.ridden[pid] <= trip.reference_m + trip.budget_m + EPSILON, "Cumulative personal budget exceeded"
                if pid not in taxi.occupied:
                    consumed = taxi.odometer_m - commitment.confirmation_odometer_m
                    assert consumed <= commitment.approach_limit_m + EPSILON, "Approach promise exceeded"
        for passenger in self.passengers:
            assert passenger.initial_calls <= 1, "Repeated CFP for a persistent request"
            state = passenger.state
            if state in (PassengerState.RESERVED, PassengerState.BOARDING,
                         PassengerState.ONBOARD, PassengerState.ALIGHTING):
                taxi = assignments[passenger.passenger_id]
                assert taxi.taxi_id == passenger.taxi_id, "Agent assignment disagreement"
                assert (passenger.passenger_id in taxi.occupied) == (state != PassengerState.RESERVED)
            if state == PassengerState.DELIVERED:
                assert passenger.passenger_id not in assignments
                assert passenger.dates["drop_end"] is not None
                assert passenger.distance_m <= passenger.trip.reference_m + passenger.trip.budget_m + EPSILON
            dates = [passenger.trip.appearance_tick * STEP_SECONDS]
            dates.extend(v for v in passenger.dates.values() if v is not None)
            assert dates == sorted(dates), "Passenger chronology is inconsistent"
