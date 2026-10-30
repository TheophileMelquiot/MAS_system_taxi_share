"""Environmental interaction, independent of sequential taxi activation."""

from collections import Counter
from .contracts import Move
from .config import FREE_SPEED_MPS


def traffic_snapshot(taxis, threshold):
    """Compute directed loads and speeds once for the next shared interval.

    Only taxis with a Move count, including newly started moves. A -> B and
    B -> A have independent loads, even when a taxi can reverse at a boundary.
    threshold is K in speed = free_speed / max(1, load / K); it does not cap
    entry or model physical queues. Parked and service taxis do not count.
    """
    loads = Counter((taxi.action.origin, taxi.action.target)
                    for taxi in taxis if isinstance(taxi.action, Move))
    # One taxi counts as one vehicle, irrespective of its passenger count.
    # Freeze all speeds before any taxi advances to avoid activation-order bias.
    speeds = {edge: FREE_SPEED_MPS / max(1.0, count / threshold)
              for edge, count in loads.items()}
    return loads, speeds
