r"""Run one simulation without opening the graphical interface.

Use this script to export a complete run or try Config parameters from the
command line. For example, from the repository root in PowerShell:
    .\.venv\Scripts\python.exe run_simulation.py --output output/single-run

Run app.py for interactive exploration, or run_experiments.py for the paired
capacity comparison. Use --help to list configuration overrides and exports.
"""

import argparse
import json
from pathlib import Path
from taxishare.config import Config
from taxishare.scenario import generate
from taxishare.model import TaxiShareModel
from taxishare.metrics import export_results, summary


def main():
    """Read parameters, generate inputs, run to a stopping condition and export.

    Command-line overrides take precedence over --config JSON values. That JSON
    contains generation parameters, not a saved map or passenger scenario.
    Return 0 when everyone is delivered, 2 for an incomplete run or CLI error.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, help="JSON object with Config fields")
    parser.add_argument("--output", type=Path, default=Path("output/latest"))
    parser.add_argument("--trace-messages", action="store_true")
    parser.add_argument("--no-figure", action="store_true")
    for name, field in Config.__dataclass_fields__.items():
        # Expose the same parameters as Config without maintaining a second list.
        parser.add_argument("--" + name.replace("_", "-"), dest=name, type=type(field.default), default=None)
    args = parser.parse_args()
    overrides = {name: getattr(args, name) for name in Config.__dataclass_fields__ if getattr(args, name) is not None}
    try:
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
