"""End-to-end contracts at physical boundaries and message round boundaries."""

from dataclasses import replace
import pytest
from taxishare.config import Config, FREE_SPEED_MPS
from taxishare.contracts import Move, Operation, PassengerState, Trip, Stop, Commitment
from taxishare.messaging import Kind, MessageBus
from taxishare.model import TaxiShareModel
from taxishare.metrics import summary, passenger_rows, taxi_rows, export_results
from taxishare.planning import PlanningContext, InsertionPlanner
from taxishare.scenario import generate
from taxishare.traffic import traffic_snapshot


def test_single_trip_exact_durations(ring_scenario):
    model = TaxiShareModel(ring_scenario()).run_to_end()
    row = passenger_rows(model)[0]
    assert model.status == "complete"
    assert model.time_seconds == 40
    assert row["board_start_seconds"] == pytest.approx(7.2)
    assert row["board_end_seconds"] == pytest.approx(9.2)
    assert row["drop_start_seconds"] == pytest.approx(38)
    assert row["drop_end_seconds"] == 40
    assert row["distance_ridden_m"] == pytest.approx(400)
    assert row["boarding_seconds"] == pytest.approx(2)
    assert row["alighting_seconds"] == pytest.approx(2)
    assert row["total_seconds"] == pytest.approx(row["waiting_seconds"] + row["onboard_seconds"] + 4)


def test_boundary_has_no_double_progress_and_seat_timing(ring_scenario):
    model = TaxiShareModel(ring_scenario())
    taxi, passenger = model.taxis[0], model.passengers[0]
    for _ in range(36):
        model.step()
    assert model.tick == 36
    assert isinstance(taxi.action, Move)
    assert taxi.action.progressed_m == pytest.approx(100)
    assert passenger.state == PassengerState.RESERVED
    model.step()
    assert passenger.state == PassengerState.BOARDING
    assert taxi.occupied == {0}
    assert taxi.action.remaining_ticks == 9
    for _ in range(9):
        model.step()
    assert taxi.action.remaining_ticks == 0
    model.step()
    assert passenger.state == PassengerState.ONBOARD
    assert taxi.action.progressed_m == pytest.approx(FREE_SPEED_MPS * 0.2)
    while passenger.state != PassengerState.ALIGHTING:
        model.step()
    assert 0 in taxi.occupied
    for _ in range(9):
        model.step()
    assert 0 in taxi.occupied
    model.step()
    assert not taxi.occupied
    assert passenger.state == PassengerState.DELIVERED


def test_future_request_prevents_early_stop(ring_scenario):
    model = TaxiShareModel(ring_scenario(requests=((0, 0, 2, 50),)))
    for _ in range(50):
        model.step()
        assert model.running
        assert model.passengers[0].state == PassengerState.FUTURE
        assert not model.taxis[0].known_requests
    model.run_to_end()
    assert model.time_seconds == 50


def test_no_requests_and_null_statistics(ring_scenario):
    model = TaxiShareModel(ring_scenario(requests=())).run_to_end()
    result = summary(model)
    assert model.time_seconds == 0 and model.status == "complete"
    assert result["mean_waiting_seconds"] is None
    assert result["shared_distance_rate"] is None
    assert result["distance_empty_m"] == 0


def test_frozen_state_is_incomplete_not_abandonment(ring_scenario, monkeypatch):
    model = TaxiShareModel(ring_scenario(fleet=((0, (1, 0), (-1, 0)),)))
    # Exercise the defensive diagnostic independently of initial orientation.
    monkeypatch.setattr(model.planner, "best_plan", lambda *args: (None, "no_feasible_offer"))
    model.run_to_end()
    assert model.stop_reason == "frozen_no_feasible_offer"
    assert model.time_seconds == 0
    assert model.passengers[0].state == PassengerState.WAITING
    assert model.taxis[0].pos == (1, 0)
    assert model.taxis[0].heading == (-1, 0)


def test_limit_keeps_partial_distance_and_missing_dates(ring_scenario, tmp_path):
    model = TaxiShareModel(ring_scenario(max_seconds=10)).run_to_end()
    row = passenger_rows(model)[0]
    assert model.stop_reason == "time_limit"
    assert row["state"] == "onboard" and row["distance_ridden_m"] > 0
    assert row["drop_end_seconds"] is None and row["total_seconds"] is None
    assert row["detour_m"] is None
    export_results(model, tmp_path, figure=False)
    assert "incomplete" in (tmp_path / "summary.json").read_text()


def test_simultaneous_calls_single_assignment_and_no_repeated_cfp(ring_scenario):
    scenario = ring_scenario(requests=((0, 0, 2, 0), (1, 0, 2, 0), (2, 0, 2, 0)), capacity=2)
    model = TaxiShareModel(scenario, trace_messages=True).run_to_end()
    assert model.status == "complete"
    assert all(p.initial_calls == 1 for p in model.passengers)
    assert model.bus.counts["CFP"] == 3
    assert model.bus.counts["CONFIRM"] == 3
    assert model.bus.counts["REJECT"] >= 1
    assert sum(model.taxis[0].distances[2:]) > 0
    assert any(m.kind == Kind.REJECT for m in model.bus.history)
    assert model.bus.empty()
    assert not model.taxis[0].known_requests and not model.taxis[0].offers


def test_independent_actions_and_existing_move_kept_on_insertion(ring_scenario):
    model = TaxiShareModel(ring_scenario(requests=((0, 0, 2, 0), (1, 1, 2, 1)),
        fleet=((0, (0, 0), (0, -1)), (1, (0, 6), (0, 1)))))
    model.step()
    moving = model.taxis[0]
    original = moving.action
    model.step()
    assert moving.action is original
    assert original.progressed_m == pytest.approx(2 * FREE_SPEED_MPS * 0.2)
    assert model.taxis[1].idle_seconds > 0
    model.run_to_end()


def test_stale_acceptance_never_creates_commitment(ring_scenario):
    model = TaxiShareModel(ring_scenario(requests=()))
    taxi = model.taxis[0]
    model.bus.send(("passenger", 999), taxi.address, Kind.ACCEPT, 0, (999, taxi.taxi_id, -1))
    taxi.process_acceptances()
    assert not taxi.commitments
    assert model.bus.receive(("passenger", 999), {Kind.REJECT})[0].payload[1] == "expired_or_unknown_offer"


def test_independent_mailboxes():
    bus = MessageBus()
    bus.send(("passenger", 0), ("taxi", 0), Kind.CFP, 0, "trip")
    bus.send(("passenger", 0), ("taxi", 1), Kind.CFP, 0, "trip")
    assert len(bus.receive(("taxi", 0), {Kind.CFP})) == 1
    assert len(bus.receive(("taxi", 0), {Kind.CFP})) == 0
    assert len(bus.receive(("taxi", 1), {Kind.CFP})) == 1


def test_snapshot_shared_speeds_and_distinct_directions(ring_scenario):
    fleet = tuple((i, (i, 0), (1, 0) if i else (0, -1)) for i in range(4))
    model = TaxiShareModel(ring_scenario(fleet=fleet, requests=()))
    for taxi in model.taxis[:3]:
        taxi.action = Move((1, 0), (2, 0), (1, 0))
    model.taxis[3].action = Move((2, 0), (1, 0), (-1, 0))
    loads, speeds = traffic_snapshot(model.taxis, 2)
    assert loads[((1, 0), (2, 0))] == 3
    assert speeds[((1, 0), (2, 0))] == pytest.approx(FREE_SPEED_MPS / 1.5)
    assert speeds[((2, 0), (1, 0))] == FREE_SPEED_MPS
    for taxi in reversed(model.taxis):
        taxi.advance_action(speeds)
    assert len({t.action.progressed_m for t in model.taxis[:3]}) == 1


def test_quantization_and_congestion_are_separated(ring_scenario):
    model = TaxiShareModel(ring_scenario(requests=()))
    taxi = model.taxis[0]
    taxi.action = Move((0, 0), (1, 0), (1, 0), 99)
    taxi._advance_move(FREE_SPEED_MPS / 3)
    taxi._advance_move(FREE_SPEED_MPS / 3)
    assert taxi.odometer_m == pytest.approx(1)
    assert taxi.moving_seconds == pytest.approx(0.4)
    assert taxi.congestion_seconds == pytest.approx(1 / (FREE_SPEED_MPS / 3) - 1 / FREE_SPEED_MPS)
    assert taxi.quantization_seconds == pytest.approx(0.4 - 1 / (FREE_SPEED_MPS / 3))


def test_capacity_is_reusable_and_commitments_can_exceed_capacity(ring_scenario):
    city = ring_scenario().city()
    trip_a = Trip(0, (1, 0), (3, 0), 0, 200, 50)
    trip_b = Trip(1, (3, 0), (5, 0), 0, 200, 50)
    commitment = Commitment(trip_a, 0, 0)
    context = PlanningContext((1, 0), 0, 0, 0, 0, frozenset(), {0: 0},
        {0: commitment}, (Stop(0, True, (1, 0)), Stop(0, False, (3, 0))), 1)
    plan, _ = InsertionPlanner(city).best_plan(context, trip_b)
    assert plan is not None
    assert [(l.stop.passenger_id, l.stop.pickup) for l in plan.legs] == [(0, True), (0, False), (1, True), (1, False)]


def test_cumulative_budget_and_approach_protection(ring_scenario):
    city = ring_scenario().city()
    original = Trip(0, (1, 0), (5, 0), 0, 400, 100)
    candidate = Trip(1, (3, 0), (5, 0), 0, 200, 50)
    context = PlanningContext((3, 0), 20, 0, 0, 300, frozenset({0}), {0: 301},
        {0: Commitment(original, 0, 100)}, (Stop(0, False, (5, 0)),), 2)
    plan, _ = InsertionPlanner(city).best_plan(context, candidate)
    assert plan is None  # 301 already ridden + 200 remaining exceeds 500.
    context = replace(context, occupied=frozenset(), ridden={0: 0},
                      stops=(Stop(0, True, (5, 0)), Stop(0, False, (1, 0))))
    plan, _ = InsertionPlanner(city).best_plan(context, candidate)
    assert plan is None  # Prior approach consumption cannot be reset.


def test_replay_render_and_exports_do_not_change_outcomes(ring_scenario, tmp_path):
    from taxishare.visualization import create_figure, draw_model
    scenario = ring_scenario(requests=((0, 0, 2, 0), (1, 1, 2, 20)))
    first = TaxiShareModel(scenario).run_to_end()
    second = TaxiShareModel(scenario)
    for _ in range(10):
        second.step()
    before = (second.tick, second.scenario.fingerprint, second.random.getstate())
    draw_model(create_figure(), second)
    export_results(second, tmp_path, figure=True)
    assert (second.tick, second.scenario.fingerprint, second.random.getstate()) == before
    second.run_to_end()
    assert summary(first) == summary(second)
    assert passenger_rows(first) == passenger_rows(second)
    assert taxi_rows(first) == taxi_rows(second)


def test_distance_categories_sum_and_weighted_sharing(ring_scenario):
    model = TaxiShareModel(ring_scenario(requests=((0, 0, 2, 0), (1, 0, 2, 0)))).run_to_end()
    taxi = model.taxis[0]
    assert sum(taxi.distances) == pytest.approx(taxi.odometer_m)
    result = summary(model)
    assert result["shared_distance_rate"] == pytest.approx(sum(taxi.distances[2:]) / taxi.odometer_m)


def test_default_sixty_requests_finish_with_all_invariants():
    model = TaxiShareModel(generate(Config())).run_to_end()
    assert model.status == "complete"
    assert len(passenger_rows(model)) == 60
    assert len(taxi_rows(model)) == 8
    assert summary(model)["delivered_count"] == 60


def test_operation_is_not_restarted_by_new_reservation(ring_scenario):
    model = TaxiShareModel(ring_scenario(requests=((0, 0, 2, 0), (1, 0, 2, 40))))
    for _ in range(40):
        model.step()
    taxi = model.taxis[0]
    operation = taxi.action
    assert isinstance(operation, Operation) and operation.remaining_ticks == 6
    model.step()
    assert taxi.action is operation and operation.remaining_ticks == 5
    assert model.passengers[1].state == PassengerState.RESERVED
    model.run_to_end()
    assert model.passengers[0].dates["board_end"] == pytest.approx(9.2)


def test_full_taxi_releases_seat_only_after_drop(ring_scenario):
    scenario = ring_scenario(requests=((0, 0, 1, 0), (1, 1, 2, 0)), capacity=1)
    model = TaxiShareModel(scenario).run_to_end()
    first, second = model.passengers
    assert second.dates["board_start"] == first.dates["drop_end"]
    assert second.dates["board_start"] == first.dates["drop_start"] + 2
    assert model.taxis[0].distances[1] == pytest.approx(400)


def test_eta_uses_free_speed_and_remaining_operation(ring_scenario):
    model = TaxiShareModel(ring_scenario())
    taxi = model.taxis[0]
    model.step()
    context = taxi.planning_context()
    assert context.locked_seconds == pytest.approx((100 - FREE_SPEED_MPS * 0.2) / FREE_SPEED_MPS)
    for _ in range(36):
        model.step()
    assert taxi.planning_context().locked_seconds == pytest.approx(1.8)


def test_offer_ranking_is_pickup_then_max_budget_then_taxi_id(ring_scenario):
    from taxishare.contracts import Offer, Plan
    model = TaxiShareModel(ring_scenario())
    passenger = model.passengers[0]
    passenger.announce()
    for taxi_id, eta, score in ((0, 30, 0.1), (1, 25, 0.5), (2, 25, 0.2), (3, 25, 0.2)):
        plan = Plan((), 100, 100, eta, 400, score)
        model.bus.send(("taxi", taxi_id), passenger.address, Kind.OFFER, 0, Offer(0, taxi_id, 0, plan))
    passenger.choose_offer()
    assert passenger.selected_offer.taxi_id == 2


def test_zero_budget_allows_exact_route_sharing(ring_scenario):
    model = TaxiShareModel(ring_scenario(requests=((0, 0, 2, 0), (1, 0, 2, 0)), detour_rate=0)).run_to_end()
    assert model.status == "complete"
    assert model.taxis[0].distances[2] == pytest.approx(400)


def test_congestion_end_to_end_and_activation_order_independence(ring_scenario):
    # Two taxis independently reserve sequential trips on the same directed road.
    # K=0.5 also slows a single vehicle, producing a controlled nonzero signal.
    scenario = ring_scenario(requests=((0, 0, 2, 0), (1, 1, 2, 0)),
        fleet=((0, (0, 0), (0, -1)), (1, (2, 0), (1, 0))), capacity=1,
        congestion_threshold=0.5)
    first = TaxiShareModel(scenario).run_to_end()
    second = TaxiShareModel(scenario)
    # Reverse both the environmental traversal and Mesa's activation order.
    second.taxis.reverse()
    second.agents_by_type[type(second.taxis[0])].sort("taxi_id", ascending=False, inplace=True)
    second.run_to_end()
    assert summary(first) == summary(second)
    assert passenger_rows(first) == passenger_rows(second)
    assert summary(first)["congestion_vehicle_seconds"] > 0


def test_acceptance_keeps_announced_offer_bounds(ring_scenario):
    model = TaxiShareModel(ring_scenario(requests=((0, 0, 2, 0), (1, 0, 2, 0)), capacity=1),
                          trace_messages=True)
    model.step()
    assert model.passengers[0].state == PassengerState.RESERVED
    assert model.passengers[1].state == PassengerState.WAITING
    assert model.bus.counts["REJECT"] == 1
    # No second negotiation is performed at t=0; the rejected trip persists.
    assert model.tick == 1 and model.passengers[1].initial_calls == 1


def test_direct_approach_can_reverse_after_pickup():
    from taxishare.city import City
    city = City(7, 7, (0, 3, 6), (0, 3, 6))
    trip = Trip(0, (1, 0), (2, 0), 0, 100, 25)
    context = PlanningContext((4, 0), 0, 0, 0, 0, frozenset(), {}, {}, (), 3)
    plan, _ = InsertionPlanner(city).best_plan(context, trip)
    assert plan is not None
    assert plan.candidate_approach_m == 300
    assert plan.legs[0].cells == ((3, 0), (2, 0), (1, 0))
    assert plan.legs[1].cells == ((2, 0),)
    assert plan.candidate_ride_m == 100


def test_four_passengers_and_zero_actual_wait(ring_scenario):
    model = TaxiShareModel(ring_scenario(requests=tuple((i, 0, 2, 0) for i in range(4)),
        fleet=((0, (1, 0), (1, 0)),), capacity=4)).run_to_end()
    assert model.status == "complete"
    assert model.taxis[0].distances[4] == pytest.approx(400)
    assert min(p["waiting_seconds"] for p in passenger_rows(model)) == 0


def test_parked_taxi_can_reverse_to_serve_same_cell_pickup(ring_scenario):
    model = TaxiShareModel(ring_scenario(fleet=((0, (1, 0), (-1, 0)),))).run_to_end()
    assert model.status == "complete"
    assert passenger_rows(model)[0]["board_start_seconds"] == 0
    assert model.taxis[0].odometer_m == pytest.approx(400)


def test_reversal_waits_for_locked_portion_and_preserves_prefix(ring_scenario):
    model = TaxiShareModel(ring_scenario(requests=()))
    taxi = model.taxis[0]
    action = Move((0, 0), (1, 0), (1, 0), 25)
    taxi.action = action
    context = taxi.planning_context()
    assert context.anchor == (1, 0)
    assert context.prefix_distance_m == 75
    trip = Trip(0, (0, 0), (1, 0), 0, 100, 25)
    plan, _ = model.planner.best_plan(context, trip)
    assert plan.candidate_approach_m == 175
    taxi.legs = list(plan.legs)
    taxi.start_action()
    assert taxi.action is action and taxi.action.progressed_m == 25
    action.progressed_m = 100
    taxi.finalize_action()
    taxi.start_action()
    assert taxi.action.origin == (1, 0)
    assert taxi.action.target == (0, 0)
    assert taxi.action.heading == (-1, 0)


@pytest.mark.parametrize("field", ["candidate_approach_m", "candidate_pickup_seconds",
                                   "candidate_ride_m", "budget_score"])
def test_revalidation_preserves_each_announced_bound(ring_scenario, field):
    city = ring_scenario().city()
    trip = Trip(0, (1, 0), (5, 0), 0, 400, 100)
    context = PlanningContext((0, 0), 0, 0, 0, 0, frozenset(), {}, {}, (), 3)
    planner = InsertionPlanner(city)
    plan, _ = planner.best_plan(context, trip)
    assert planner.best_plan(context, trip, plan)[0] == plan
    stricter = replace(plan, **{field: getattr(plan, field) - 1})
    assert planner.best_plan(context, trip, stricter)[0] is None


def test_locked_prefix_counts_against_onboard_passenger_budget(ring_scenario):
    original = Trip(0, (1, 0), (3, 0), 0, 200, 50)
    candidate = Trip(1, (2, 0), (3, 0), 0, 100, 25)
    context = PlanningContext((2, 0), 0, 75, 75 / FREE_SPEED_MPS, 100,
        frozenset({0}), {0: 100}, {0: Commitment(original, 0, 0)},
        (Stop(0, False, (3, 0)),), 2)
    planner = InsertionPlanner(ring_scenario().city())
    assert planner.best_plan(context, candidate)[0] is None  # 100 + 75 + 100 > 250.
    assert planner.best_plan(replace(context, prefix_distance_m=0), candidate)[0] is not None
