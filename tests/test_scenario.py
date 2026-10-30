"""Generation, input rejection and legal oriented reachability."""

from dataclasses import replace
import json
import pytest
from taxishare.config import Config
from taxishare.city import Building, City
from taxishare.scenario import generate, TaxiInitial


@pytest.mark.parametrize("options", [dict(capacity=5), dict(taxis=0), dict(width=6),
    dict(axis_spacing=1), dict(appearance_seconds=0.3), dict(congestion_threshold=0),
    dict(max_seconds=float("nan")), dict(requests=-1), dict(capacity=True)])
def test_invalid_configuration_is_rejected(options):
    with pytest.raises(ValueError):
        Config(**options)


def test_four_random_streams_are_isolated():
    first = generate(Config())
    second = generate(Config(taxis=12))
    assert first.horizontal == second.horizontal
    assert first.vertical == second.vertical
    assert first.buildings == second.buildings
    assert first.requests == second.requests
    changed_times = generate(Config(appearance_seconds=600))
    assert [(r.origin_id, r.destination_id) for r in first.requests] == [
        (r.origin_id, r.destination_id) for r in changed_times.requests]
    assert first.fleet == changed_times.fleet


def test_scenario_export_preserves_complete_generated_inputs(tmp_path):
    scenario = generate(Config(requests=3))
    path = tmp_path / "scenario.json"
    scenario.save(path)
    # JSON turns tuples into arrays. Compare the complete exported inputs in
    # that representation without recreating a scenario-file loading feature.
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert raw == json.loads(json.dumps(scenario.to_dict()))
    assert generate(scenario.config).fingerprint == scenario.fingerprint


def test_generated_defaults_and_accesses():
    scenario = generate(Config())
    city = scenario.validate()
    assert len(scenario.fleet) == len({t.cell for t in scenario.fleet}) == 8
    assert len(scenario.buildings) == 32 and len(scenario.requests) == 60
    assert scenario.horizontal[0] == scenario.vertical[0] == 0
    assert scenario.horizontal[-1] == scenario.vertical[-1] == 20
    assert all(len(city.adjacent[b.access]) < 3 for b in scenario.buildings)
    assert all(0 <= r.appearance_tick <= 1500 for r in scenario.requests)


def test_same_access_trip_and_invalid_placement(ring_scenario):
    scenario = ring_scenario()
    request = replace(scenario.requests[0], destination_id=0)
    with pytest.raises(ValueError, match="request"):
        replace(scenario, requests=(request,)).validate()
    with pytest.raises(ValueError, match="taxi"):
        replace(scenario, fleet=(TaxiInitial(0, (2, 2), (1, 0)),)).validate()
    invalid = Building(0, (1, 1), (2, 0))
    with pytest.raises(ValueError, match="building"):
        replace(scenario, buildings=(invalid,) + scenario.buildings[1:]).validate()


def test_excessive_buildings_and_taxis_are_not_silently_reduced():
    for config in (Config(buildings=10000), Config(taxis=10000)):
        with pytest.raises(ValueError):
            generate(config)


def test_no_uturns_corners_and_personal_reference(ring_scenario):
    city = ring_scenario().validate()
    state = ((1, 0), (-1, 0))
    assert ((2, 0), (1, 0)) not in city.successors(state)
    assert city.successors(((0, 0), (-1, 0))) == (((0, 1), (0, 1)),)
    assert city.reference_distance((1, 0), (5, 0)) == 400
    assert min(len(path) for path, _ in city.paths_to(state, (5, 0))) == 20


def test_oriented_validation_rejects_dead_ends():
    city = City(4, 3, (0,), (), (Building(0, (1, 1), (1, 0)),))
    with pytest.raises(ValueError, match="continuation"):
        city.validate_oriented_accessibility()


def test_accessibility_targets_positions_not_all_headings(ring_scenario):
    # A ring has two oriented components; both reach every access position.
    ring_scenario().validate()


def test_boolean_coordinates_and_identifiers_are_invalid(ring_scenario):
    scenario = ring_scenario()
    taxi = replace(scenario.fleet[0], cell=(False, 0))
    with pytest.raises(ValueError, match="taxi"):
        replace(scenario, fleet=(taxi,)).validate()
    request = replace(scenario.requests[0], origin_id=False)
    with pytest.raises(ValueError, match="request"):
        replace(scenario, requests=(request,)).validate()
