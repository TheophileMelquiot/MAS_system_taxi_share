"""Check paired inputs, incomplete service and honest aggregate statistics."""

from dataclasses import replace
import json
import math

import pytest
import run_experiments as experiments


def test_compare_generates_once_and_reuses_inputs(ring_scenario, monkeypatch, tmp_path):
    scenario = ring_scenario(requests=((0, 0, 2, 0), (1, 0, 2, 0)))
    generated = []

    def generate(config):
        generated.append(config.seed)
        return replace(scenario, config=config)

    monkeypatch.setattr(experiments, "generate", generate)
    rows = experiments.compare(scenario.config, [7, 8], tmp_path)
    assert generated == [7, 8]
    assert all(row["included"] for row in rows)
    for seed in generated:
        individual = json.loads((tmp_path / f"seed-{seed}/individual/scenario.json").read_text())
        shared = json.loads((tmp_path / f"seed-{seed}/shared/scenario.json").read_text())
        assert individual["config"].pop("capacity") == 1
        assert shared["config"].pop("capacity") == 3
        # Compare every saved input, including geometry and appearance ticks.
        assert individual == shared
    assert all(row["individual_shared_distance_rate"] == 0 for row in rows)
    assert all(row["shared_shared_distance_rate"] > 0 for row in rows)
    assert (tmp_path / "comparison.csv").is_file()
    assert (tmp_path / "summary.csv").is_file()
    assert json.loads((tmp_path / "study.json").read_text())["complete_pairs"] == 2


def test_incomplete_pairs_keep_exports_but_have_no_deltas(ring_scenario, monkeypatch, tmp_path):
    scenario = ring_scenario(max_seconds=0.2)
    monkeypatch.setattr(experiments, "generate", lambda config: replace(scenario, config=config))
    rows = experiments.compare(scenario.config, [7], tmp_path)
    assert not rows[0]["included"]
    assert all(rows[0][f"delta_{metric}"] is None for metric in experiments.METRICS)
    assert all(row["pair_count"] == 0 and row["mean_delta"] is None
               for row in experiments.aggregate(rows))
    assert (tmp_path / "seed-7/shared/passengers.csv").is_file()
    assert json.loads((tmp_path / "study.json").read_text())["excluded_seeds"] == [7]


def test_aggregate_uses_sample_deviation_of_paired_differences():
    rows = []
    for individual, shared in ((10, 8), (20, 24)):
        row = {"included": True}
        for metric in experiments.METRICS:
            row.update({f"individual_{metric}": individual,
                        f"shared_{metric}": shared, f"delta_{metric}": shared - individual})
        rows.append(row)
    for result in experiments.aggregate(rows):
        assert result["pair_count"] == 2
        assert result["mean_delta"] == 1
        assert result["sd_delta"] == pytest.approx(math.sqrt(18))
    assert all(row["sd_delta"] is None for row in experiments.aggregate(rows[:1]))


def test_empty_demand_keeps_zero_distance_and_missing_trip_statistics(ring_scenario, monkeypatch, tmp_path):
    scenario = ring_scenario(requests=())
    monkeypatch.setattr(experiments, "generate", lambda config: replace(scenario, config=config))
    rows = experiments.compare(scenario.config, [7], tmp_path)
    assert rows[0]["included"]
    assert rows[0]["delta_distance_total_m"] == 0
    assert rows[0]["delta_mean_total_seconds"] is None
    statistics = {row["metric"]: row for row in experiments.aggregate(rows)}
    assert statistics["distance_total_m"]["pair_count"] == 1
    assert statistics["mean_total_seconds"]["pair_count"] == 0


@pytest.mark.parametrize("seeds", [[], [7, 7], [-1]])
def test_invalid_seed_lists_are_rejected_before_running(ring_scenario, tmp_path, seeds):
    with pytest.raises(ValueError):
        experiments.compare(ring_scenario().config, seeds, tmp_path)
