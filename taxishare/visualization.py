"""Read-only Matplotlib views shared by Tk and image exports."""

from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.offsetbox import AnnotationBbox, DrawingArea
from matplotlib.patches import Circle
from collections import defaultdict
from .contracts import Move, PassengerState

COLORS = {"idle": "#78869b", "reserved": "#e9a33b", "approach": "#e9a33b",
          "occupied": "#168b91", "boarding": "#7355b7", "alighting": "#d56e48"}
PASSENGER_COLORS = {PassengerState.WAITING: "#db4668", PassengerState.RESERVED: "#326bd1"}


def create_figure():
    return Figure(figsize=(12, 7), facecolor="#f4f6fa", layout="constrained")


def draw_model(figure, model):
    """No random draws, time advancement or decision changes are allowed here."""
    figure.clear()
    layout = figure.add_gridspec(3, 2, width_ratios=(1.5, 1), height_ratios=(1, 1, 0.35))
    city_ax = figure.add_subplot(layout[:2, 0])
    legend_ax = figure.add_subplot(layout[2, 0])
    service_ax = figure.add_subplot(layout[0, 1])
    distance_ax = figure.add_subplot(layout[1, 1])
    _draw_city(city_ax, model)
    _draw_service(service_ax, model)
    _draw_distances(distance_ax, model)
    _draw_legends(legend_ax)
    figure.suptitle(f"TaxiShare  |  {model.time_seconds:.1f} s  |  {model.status}",
                   fontsize=15, fontweight="bold", color="#192c45")


def _draw_city(ax, model):
    city = model.city
    ax.set_facecolor("#e5ebdf")
    for y in city.horizontal:
        ax.plot([0, city.width - 1], [y, y], color="#ffffff", linewidth=7, zorder=1)
        ax.plot([0, city.width - 1], [y, y], color="#c3cbd3", linewidth=1, zorder=1)
    for x in city.vertical:
        ax.plot([x, x], [0, city.height - 1], color="#ffffff", linewidth=7, zorder=1)
        ax.plot([x, x], [0, city.height - 1], color="#c3cbd3", linewidth=1, zorder=1)
    for b in city.buildings:
        ax.plot([b.cell[0], b.access[0]], [b.cell[1], b.access[1]], color="#a5aeb7", linewidth=0.7)
    ax.scatter([b.cell[0] for b in city.buildings], [b.cell[1] for b in city.buildings],
               marker="s", s=35, color="#526476", zorder=2)
    ax.scatter([b.access[0] for b in city.buildings], [b.access[1] for b in city.buildings],
               marker=".", s=18, color="#526476", zorder=2)
    _draw_waiting_passengers(ax, model)
    _draw_taxis(ax, model)
    ax.set(xlim=(-1, city.width), ylim=(-1, city.height), aspect="equal",
           xlabel="Cells (100 m)", ylabel="Cells (100 m)", title="City, access points and headings")


def _draw_waiting_passengers(ax, model):
    """One fixed-size dot per person, in an ID-ordered row beside each access.

    Offsets are measured in display points, so dots remain separated when the
    window is resized. A leader connects the row to the actual access; these
    visual offsets never change passenger positions in the simulation.
    """
    groups = defaultdict(list)
    for passenger in model.passengers:
        if passenger.state in PASSENGER_COLORS:
            groups[passenger.trip.origin].append(passenger)
    for access, passengers in sorted(groups.items()):
        passengers.sort(key=lambda p: p.passenger_id)
        row = DrawingArea(len(passengers) * 10, 10)
        for index, passenger in enumerate(passengers):
            row.add_artist(Circle((5 + index * 10, 5), radius=3.5,
                                  facecolor=PASSENGER_COLORS[passenger.state],
                                  edgecolor="white", linewidth=0.7))
        # Grow inward from the nearest side of the map, above the taxi markers.
        right_half = access[0] > (model.city.width - 1) / 2
        annotation = AnnotationBbox(
            row, access, xybox=(-5 if right_half else 5, 14),
            xycoords="data", boxcoords="offset points",
            box_alignment=(1 if right_half else 0, 0), frameon=False,
            arrowprops={"arrowstyle": "-", "color": "#697787", "linewidth": 0.7},
            annotation_clip=False)
        annotation.set_zorder(6)
        ax.add_artist(annotation)


def _taxi_color(taxi):
    """Occupants take priority: an occupied taxi may also have future bookings."""
    if taxi.occupied:
        return COLORS["occupied"]
    return COLORS["reserved"] if taxi.commitments else COLORS["idle"]


def _draw_taxis(ax, model):
    """Triangle direction encodes heading; color encodes occupancy/booking."""
    labels = defaultdict(list)
    for taxi in model.taxis:
        x, y = taxi.pos
        heading = taxi.heading
        if isinstance(taxi.action, Move):
            # MultiGrid keeps the origin until arrival; interpolation is only
            # visual and must not introduce extra positions into the simulation.
            ratio = taxi.action.progressed_m / 100
            heading = taxi.action.heading
            x += ratio * heading[0]
            y += ratio * heading[1]
        color = _taxi_color(taxi)
        marker = {(0, 1): "^", (1, 0): ">", (0, -1): "v", (-1, 0): "<"}[heading]
        ax.scatter([x], [y], s=90, marker=marker, color=color, edgecolors="white", zorder=4)
        labels[(round(x, 3), round(y, 3))].append(str(taxi.taxi_id))
    for position, ids in labels.items():
        ax.annotate(", ".join(ids), position, xytext=(4, 5), textcoords="offset points", fontsize=7)


def _draw_legends(ax):
    """Reserve a bottom row for two independent, clearly titled legends."""
    ax.set_axis_off()
    taxi_handles = [Line2D([], [], marker=">", markersize=8, linestyle="", color=COLORS[state], label=label)
               for state, label in (("idle", "Empty, available taxi"),
                                    ("reserved", "Empty, reserved taxi"),
                                    ("occupied", "Taxi with passengers"))]
    passenger_handles = [Line2D([], [], marker="o", linestyle="", color=color, label=label)
                   for color, label in ((PASSENGER_COLORS[PassengerState.WAITING], "Waiting passenger"),
                                        (PASSENGER_COLORS[PassengerState.RESERVED], "Reserved passenger"))]
    taxi_legend = ax.legend(handles=taxi_handles, title="Taxis", loc="upper left",
                           bbox_to_anchor=(0.04, 1), fontsize=8, title_fontsize=9)
    ax.add_artist(taxi_legend)
    ax.legend(handles=passenger_handles, title="Passengers", loc="upper right",
              bbox_to_anchor=(0.96, 1), fontsize=8, title_fontsize=9)


def _draw_service(ax, model):
    values = model.data.model_vars
    times = values["time_seconds"]
    for key, label, color in (("delivered", "Delivered", "#168b91"),
                               ("waiting", "Waiting", "#db4668"),
                               ("reserved", "Reserved", PASSENGER_COLORS[PassengerState.RESERVED])):
        ax.plot(times, values[key], label=label, color=color, linewidth=1.7)
    ax.set(title="Request service", xlabel="Simulated time (s)", ylabel="Passengers",
           xlim=(0, max(1, model.time_seconds)), ylim=(0, max(1, len(model.passengers))))
    ax.grid(alpha=0.15)
    ax.legend(fontsize=8)


def _draw_distances(ax, model):
    categories = range(model.config.capacity + 1)
    distances = [sum(t.distances[i] for t in model.taxis) / 1000 for i in categories]
    ax.bar([str(i) for i in categories], distances,
           color=["#e9a33b", "#78869b", "#168b91", "#4275a7", "#7355b7"][:len(distances)])
    ax.set(title="Distance by occupancy", xlabel="Passengers on board", ylabel="Taxi kilometres")
    ax.set_ylim(0, max(1, max(distances, default=0) * 1.1))
    ax.grid(axis="y", alpha=0.15)
