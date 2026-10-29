"""Command-line entry point for a single reproducible simulation."""

import argparse
import json
from pathlib import Path
from taxishare.config import Config
from taxishare.scenario import Scenario, generate
from taxishare.model import TaxiShareModel
from taxishare.metrics import export_results, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", type=Path, help="Load complete inputs; generation flags cannot be combined")
    parser.add_argument("--config", type=Path, help="JSON object with Config fields")
    parser.add_argument("--output", type=Path, default=Path("output/latest"))
    parser.add_argument("--trace-messages", action="store_true")
    parser.add_argument("--no-figure", action="store_true")
    for name, field in Config.__dataclass_fields__.items():
        parser.add_argument("--" + name.replace("_", "-"), dest=name, type=type(field.default), default=None)
    args = parser.parse_args()
    overrides = {name: getattr(args, name) for name in Config.__dataclass_fields__ if getattr(args, name) is not None}
    if args.scenario and (args.config or overrides):
        parser.error("A saved scenario cannot be combined with generation parameters")
    try:
        if args.scenario:
            scenario = Scenario.load(args.scenario)
        else:
            config = json.loads(args.config.read_text(encoding="utf-8")) if args.config else {}
            scenario = generate(Config(**{**config, **overrides}))
        # Save inputs before running, including when a later execution fails.
        scenario.save(args.output / "scenario.json")
        model = TaxiShareModel(scenario, trace_messages=args.trace_messages)
        model.run_to_end()
        export_results(model, args.output, figure=not args.no_figure)
    except (ValueError, TypeError, OSError) as exc:
        parser.error(str(exc))
    print(json.dumps(summary(model), indent=2))
    print(f"Exports: {args.output.resolve()}")
    return 0 if model.status == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
