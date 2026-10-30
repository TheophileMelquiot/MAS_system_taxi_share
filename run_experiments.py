r"""Run the paired one-seat versus three-seat experiment without a GUI.

Use this script to reproduce the comparison used for analysis, rather than
manually changing the capacity in app.py. From the repository root:
    .\.venv\Scripts\python.exe run_experiments.py --output output/new-comparison

Defaults: five seeds (2026 through 2030), eight taxis and sixty requests per
run. Each seed generates one set of inputs reused for both capacities. Outputs
include individual runs, per-seed differences and statistics across pairs.
"""

import argparse
from dataclasses import replace
import json
from pathlib import Path
from statistics import mean, stdev

from taxishare.config import Config
from taxishare.metrics import export_results, summary, write_csv
from taxishare.model import TaxiShareModel
from taxishare.scenario import generate


# Compare vehicle distance, passenger times and sharing. Rates remain fractions
# in [0, 1], so a difference of 0.10 means ten percentage points.
METRICS = {
    "distance_total_m": "m",
    "mean_waiting_seconds": "s",
    "mean_total_seconds": "s",
    "shared_distance_rate": "fraction",
}
MODES = {"individual": 1, "shared": 3}


def aggregate(rows):
    """Summarize paired differences, excluding incomplete pairs per metric."""
    statistics = []
    for metric, unit in METRICS.items():
        pairs = [row for row in rows
                 if row["included"] and row[f"delta_{metric}"] is not None]
        deltas = [row[f"delta_{metric}"] for row in pairs]
        statistics.append({
            "metric": metric, "unit": unit, "pair_count": len(pairs),
            "individual_mean": mean(row[f"individual_{metric}"] for row in pairs) if pairs else None,
            "shared_mean": mean(row[f"shared_{metric}"] for row in pairs) if pairs else None,
            "mean_delta": mean(deltas) if deltas else None,
            # A single pair cannot estimate variation between scenarios.
            "sd_delta": stdev(deltas) if len(deltas) > 1 else None,
        })
    return statistics


def compare(config, seeds, directory):
    """Generate once per seed; change only capacity between the two runs.

    Both runs must finish before their differences enter the statistics.
    Incomplete runs are still exported so missing service remains visible.
    Matching is enforced by reusing scenario data, not by generating twice
    from the same seed. Only capacity changes within a pair.
    """
    seeds = list(seeds)
    if not seeds or any(type(seed) is not int or seed < 0 for seed in seeds):
        raise ValueError("Provide at least one nonnegative integer seed")
    if len(set(seeds)) != len(seeds):
        raise ValueError("Seeds must be distinct to avoid counting a scenario twice")
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    study = {"config": replace(config, capacity=3).to_dict(), "seeds": seeds,
             "capacities": MODES, "delta": "shared minus individual",
             "standard_deviation": "sample, across paired differences",
             "metrics": METRICS}
    manifest = directory / "study.json"
    manifest.write_text(json.dumps(study, indent=2), encoding="utf-8")
    rows = []
    for seed in seeds:
        scenario = generate(replace(config, seed=seed, capacity=3))
        results = {}
        for mode, capacity in MODES.items():
            # Reuse all exogenous inputs, rather than relying on two generators
            # to consume randomness identically. Each model creates fresh agents.
            paired = replace(scenario, config=replace(scenario.config, capacity=capacity))
            target = directory / f"seed-{seed}" / mode
            paired.save(target / "scenario.json")
            model = TaxiShareModel(paired).run_to_end()
            export_results(model, target, figure=False)
            results[mode] = summary(model)
            print(f"Seed {seed} | {mode}: {model.status} | "
                  f"{results[mode]['delivered_count']}/{results[mode]['planned_count']} delivered",
                  flush=True)
        included = all(result["status"] == "complete" for result in results.values())
        row = {"seed": seed, "planned_count": len(scenario.requests), "included": included}
        for mode, result in results.items():
            for field in ("status", "stop_reason", "delivered_count", "scenario_sha256", *METRICS):
                row[f"{mode}_{field}"] = result[field]
        for metric in METRICS:
            individual, shared = row[f"individual_{metric}"], row[f"shared_{metric}"]
            # Missing statistics and incomplete service must never look like
            # a measured zero or a gain achieved by leaving people behind.
            row[f"delta_{metric}"] = (shared - individual
                                      if included and individual is not None and shared is not None else None)
        rows.append(row)
        # Keep completed pairs available even if a later run is interrupted.
        write_csv(directory / "comparison.csv", rows)
        write_csv(directory / "summary.csv", aggregate(rows))
    study["complete_pairs"] = sum(row["included"] for row in rows)
    study["excluded_seeds"] = [row["seed"] for row in rows if not row["included"]]
    manifest.write_text(json.dumps(study, indent=2), encoding="utf-8")
    return rows


def main():
    """Parse experiment settings; return 0 for complete pairs, otherwise 2."""
    defaults = Config()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, nargs="+", default=list(range(2026, 2031)))
    parser.add_argument("--taxis", type=int, default=defaults.taxis)
    parser.add_argument("--requests", type=int, default=defaults.requests)
    parser.add_argument("--appearance-seconds", type=float, default=defaults.appearance_seconds)
    parser.add_argument("--max-seconds", type=float, default=defaults.max_seconds)
    parser.add_argument("--output", type=Path, default=Path("output/comparison"))
    args = parser.parse_args()
    try:
        config = replace(defaults, taxis=args.taxis, requests=args.requests,
                         appearance_seconds=args.appearance_seconds, max_seconds=args.max_seconds)
        rows = compare(config, args.seeds, args.output)
    except (ValueError, TypeError, OSError) as exc:
        parser.error(str(exc))
    complete = sum(row["included"] for row in rows)
    print(f"Complete pairs: {complete}/{len(rows)}. Exports: {args.output.resolve()}")
    return 0 if complete == len(rows) else 2


if __name__ == "__main__":
    raise SystemExit(main())
