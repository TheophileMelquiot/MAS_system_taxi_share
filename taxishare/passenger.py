"""Passenger decisions: one initial call, local offer choice, explicit replies."""

from mesa import Agent
from .contracts import PassengerState
from .messaging import Kind


class Passenger(Agent):
    def __init__(self, model, trip):
        super().__init__(model)
        self.trip = trip
        self.passenger_id = trip.passenger_id
        self.address = ("passenger", self.passenger_id)
        self.state = PassengerState.FUTURE
        self.taxi_id = None
        self.selected_offer = None
        self.dates = {name: None for name in ("confirmation", "board_start", "board_end", "drop_start", "drop_end")}
        self.distance_m = 0.0
        self.initial_calls = 0
        self.last_rejection = None

    def announce(self):
        """Publish exactly once, only when the scenario clock releases this trip."""
        assert self.state == PassengerState.FUTURE, "A trip may appear only once"
        self.state = PassengerState.WAITING
        self.model.grid.place_agent(self, self.trip.origin)
        for address in self.model.taxi_addresses:
            self._send(address, Kind.CFP, self.trip)
        self.initial_calls += 1

    def choose_offer(self):
        """Compare only this round's received offers, never taxi private state."""
        messages = self.model.bus.receive(self.address, {Kind.OFFER})
        if self.state != PassengerState.WAITING:
            return
        offers = [m.payload for m in messages
                  if m.payload.passenger_id == self.passenger_id
                  and m.payload.round_id == self.model.tick
                  and m.sender == ("taxi", m.payload.taxi_id)]
        if not offers:
            return
        offer = min(offers, key=lambda o: (round(o.plan.candidate_pickup_seconds, 7),
                                           round(o.plan.budget_score, 7), o.taxi_id))
        self.selected_offer = offer
        self._send(("taxi", offer.taxi_id), Kind.ACCEPT, offer.identity)

    def receive_decision(self):
        """Only confirmation creates an assignment and closes the search."""
        for message in self.model.bus.receive(self.address, {Kind.CONFIRM, Kind.REJECT}):
            if self.selected_offer is None or message.sender != ("taxi", self.selected_offer.taxi_id):
                continue
            identity, detail = message.payload
            if identity != self.selected_offer.identity or identity[2] != self.model.tick:
                continue
            if message.kind == Kind.REJECT:
                self.last_rejection = detail
                self.selected_offer = None
                continue
            assert self.state == PassengerState.WAITING, "A passenger cannot be assigned twice"
            self.taxi_id = identity[1]
            self.state = PassengerState.RESERVED
            self.dates["confirmation"] = self.model.time_seconds
            for address in self.model.taxi_addresses:
                self._send(address, Kind.CLOSE, self.passenger_id)
            self.selected_offer = None

    def receive_transport(self):
        """Transport state changes are notifications from the confirmed taxi."""
        transitions = {
            Kind.BOARD_START: (PassengerState.RESERVED, PassengerState.BOARDING, "board_start"),
            Kind.BOARD_END: (PassengerState.BOARDING, PassengerState.ONBOARD, "board_end"),
            Kind.DROP_START: (PassengerState.ONBOARD, PassengerState.ALIGHTING, "drop_start"),
            Kind.DROP_END: (PassengerState.ALIGHTING, PassengerState.DELIVERED, "drop_end"),
        }
        for message in self.model.bus.receive(self.address, set(transitions)):
            assert message.sender == ("taxi", self.taxi_id), "Unexpected transport sender"
            before, after, date = transitions[message.kind]
            assert self.state == before, f"Illegal passenger transition: {self.state} -> {after}"
            self.state = after
            self.dates[date] = self.model.time_seconds
            if message.kind == Kind.BOARD_START:
                self.model.grid.remove_agent(self)
            elif message.kind == Kind.DROP_END:
                self.distance_m = message.payload
                self.model.grid.place_agent(self, self.trip.destination)

    def _send(self, recipient, kind, payload):
        self.model.bus.send(self.address, recipient, kind, self.model.tick, payload)
