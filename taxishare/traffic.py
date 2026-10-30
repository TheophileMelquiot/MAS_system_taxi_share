"""Environmental interaction, independent of sequential taxi activation."""

from collections import Counter
from .contracts import Move
from .config import FREE_SPEED_MPS


def traffic_snapshot(taxis, threshold):
    """Include new entrants, exclude parked/service taxis, separate directions."""
    loads = Counter((taxi.action.origin, taxi.action.target)
                    for taxi in taxis if isinstance(taxi.action, Move))
    # One taxi counts as one vehicle, irrespective of its passenger count.
    # Freeze all speeds before any taxi advances to avoid activation-order bias.
    speeds = {edge: FREE_SPEED_MPS / max(1.0, count / threshold)
              for edge, count in loads.items()}
    return loads, speeds
