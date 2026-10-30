"""Observation and exports, with missing values distinct from measured zero."""

import csv
import json
from hashlib import sha256
from importlib.metadata import version
from pathlib import Path
import platform
from .config import STEP_SECONDS, EPSILON
from .contracts import PassengerState


def difference(end, start):
    return None if end is None or start is None else end - start


def passenger_rows(model):
    """One row for every planned passenger, including future/unserved clients."""
    assigned = {pid: taxi for taxi in model.taxis for pid in taxi.commitments}
    requests = {r.passenger_id: r for r in model.scenario.requests}
    rows = []
    for p in model.passengers:
        dates = p.dates
        taxi = assigned.get(p.passenger_id)
        # Ongoing distance lives in the taxi. After delivery the commitment is
        # removed and the passenger retains its final distance from DROP_END.
        distance = taxi.ridden[p.passenger_id] if taxi else p.distance_m
        completed = p.state == PassengerState.DELIVERED
        request = requests[p.passenger_id]
        rows.append({
            "passenger_id": p.passenger_id, "state": p.state.value, "taxi_id": p.taxi_id,
            "origin_building": request.origin_id, "destination_building": request.destination_id,
            "origin_access": str(p.trip.origin), "destination_access": str(p.trip.destination),
            "request_seconds": p.trip.appearance_tick * STEP_SECONDS,
            **{f"{key}_seconds": value for key, value in dates.items()},
            "reference_distance_m": p.trip.reference_m, "budget_m": p.trip.budget_m,
            "distance_ridden_m": distance,
            "detour_m": (max(0.0, distance - p.trip.reference_m)
                         if distance - p.trip.reference_m > EPSILON else 0.0) if completed else None,
            "waiting_seconds": difference(dates["board_start"], p.trip.appearance_tick * STEP_SECONDS),
            "onboard_seconds": difference(dates["drop_start"], dates["board_end"]),
            "boarding_seconds": difference(dates["board_end"], dates["board_start"]),
            "alighting_seconds": difference(dates["drop_end"], dates["drop_start"]),
            "total_seconds": difference(dates["drop_end"], p.trip.appearance_tick * STEP_SECONDS),
            "last_rejection": p.last_rejection,
        })
    return rows


def taxi_rows(model):
    rows = []
    for t in model.taxis:
        shared = sum(t.distances[2:])
        rows.append({
            "taxi_id": t.taxi_id, "state": t.status, "cell": str(t.pos), "heading": str(t.heading),
            "distance_total_m": t.odometer_m, "distance_empty_m": t.distances[0],
            **{f"distance_with_{i}_passengers_m": t.distances[i] for i in range(1, len(t.distances))},
            "distance_shared_m": shared,
            "shared_distance_rate": shared / t.odometer_m if t.odometer_m else None,
            "delivered_count": t.delivered_count,
            "moving_seconds": t.moving_seconds, "operation_seconds": t.operation_seconds,
            "idle_seconds": t.idle_seconds, "congestion_seconds": t.congestion_seconds,
            "quantization_seconds": t.quantization_seconds,
        })
    return rows


def summary(model):
    clients, taxis = passenger_rows(model), taxi_rows(model)
    # Never treat an unfinished trip's missing duration as zero: averages use
    # delivered passengers only, while the remaining population stays explicit.
    delivered = [row for row in clients if row["state"] == "delivered"]
    distance = sum(t["distance_total_m"] for t in taxis)
    shared = sum(t["distance_shared_m"] for t in taxis)
    # This is vehicle distance with at least two people, counted once per metre.
    # It is neither passenger-kilometres nor a direct measurement of emissions.
    means = {}
    for field in ("waiting_seconds", "onboard_seconds", "total_seconds", "detour_m"):
        means[f"mean_{field}"] = sum(p[field] for p in delivered) / len(delivered) if delivered else None
    return {
        "status": model.status, "stop_reason": model.stop_reason, "time_seconds": model.time_seconds,
        "scenario_sha256": model.scenario.fingerprint,
        "planned_count": len(clients), "delivered_count": len(delivered),
        "completed_trip_statistics_count": len(delivered),
        "unserved_passenger_ids": [p["passenger_id"] for p in clients if p["state"] != "delivered"],
        "distance_total_m": distance, "distance_shared_m": shared,
        "distance_empty_m": sum(t["distance_empty_m"] for t in taxis),
        "shared_distance_rate": shared / distance if distance else None,
        "congestion_vehicle_seconds": sum(t["congestion_seconds"] for t in taxis),
        "quantization_vehicle_seconds": sum(t["quantization_seconds"] for t in taxis),
        "message_counts": dict(model.bus.counts),
        "remaining_offer_failures": {str(t.taxi_id): t.last_failures for t in model.taxis if t.last_failures},
        **means,
    }


def write_csv(path, rows, fields=None):
    with Path(path).open("w", newline="", encoding="utf-8-sig") as stream:
        fieldnames = fields if fields is not None else (list(rows[0]) if rows else [])
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def provenance():
    root = Path(__file__).resolve().parents[1]
    paths = sorted((root / "taxishare").glob("*.py")) + [root / "app.py", root / "run_simulation.py"]
    hashes = {str(p.relative_to(root)): sha256(p.read_bytes()).hexdigest() for p in paths if p.exists()}
    sources = {p.name: sha256(p.read_bytes()).hexdigest() for p in root.glob("*.pdf")}
    return {"python": platform.python_version(), "platform": platform.platform(),
            "packages": {name: version(name) for name in ("mesa", "matplotlib", "numpy", "pandas", "scipy")},
            "source_sha256": hashes, "rule_document_sha256": sources,
            "rules": "U01-U71 plus current user clarifications; see docs/technical-decisions.md"}


def export_results(model, directory, *, figure=True):
    """Export partial runs honestly; exporting never advances the simulation."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    model.scenario.save(directory / "scenario.json")
    for name, payload in (("summary.json", summary(model)), ("provenance.json", provenance())):
        (directory / name).write_text(json.dumps(payload, indent=2, allow_nan=False), encoding="utf-8")
    write_csv(directory / "passengers.csv", passenger_rows(model),
              fields=None if model.passengers else ["passenger_id", "state", "taxi_id"])
    write_csv(directory / "taxis.csv", taxi_rows(model))
    model.data.get_model_vars_dataframe().to_csv(directory / "timeline.csv", index=False)
    if model.bus.trace:
        rows = [{"tick": m.tick, "sender": str(m.sender), "recipient": str(m.recipient),
                 "kind": m.kind.value, "payload": repr(m.payload)} for m in model.bus.history]
        write_csv(directory / "messages.csv", rows, ["tick", "sender", "recipient", "kind", "payload"])
    if figure:
        from .visualization import create_figure, draw_model
        fig = create_figure()
        draw_model(fig, model)
        fig.savefig(directory / "dashboard.png", dpi=150)
    return directory
