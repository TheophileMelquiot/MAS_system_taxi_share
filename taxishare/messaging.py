"""In-memory mailboxes for the passenger/taxi protocol.

Each agent has an address, such as ("passenger", 3) or ("taxi", 1). send()
appends a Message to that recipient's queue. receive(address, kinds) removes
only the requested message types, in arrival order, leaving other types for
later phases. There are no threads, network calls or simulated delivery delays.
The model's phase order determines when an agent reads and reacts to messages.

One request follows this negotiation sequence:
    passenger -> all taxis: CFP containing its Trip (sent once at appearance)
    taxis -> passenger: OFFER containing a feasible Offer for this round
    passenger -> chosen taxi: ACCEPT containing the offer identity
    chosen taxi -> passenger: CONFIRM or REJECT after revalidating the plan
    confirmed passenger -> all taxis: CLOSE containing its passenger ID

An offer identity is (passenger_id, taxi_id, round_id). CONFIRM and REJECT carry
(identity, detail), with None on confirmation or a rejection reason. Only
confirmation creates an assignment. On rejection, taxis retain the original
request and reconsider it next tick; the passenger does not send another CFP.
CLOSE removes that active request from taxi caches, not confirmed commitments.

During transport, the assigned taxi sends BOARD_START, BOARD_END, DROP_START
and DROP_END. The first three have no payload; DROP_END carries the final ride
distance. The passenger uses these events to update its state and event times.

MessageBus only delivers envelopes. Passenger and Taxi check senders and offer
identities, choose offers and update commitments. Sending does not call the
recipient's behavior. Counts and the optional history are observation tools,
not shared knowledge used to choose a taxi.
"""

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from enum import Enum

Address = tuple[str, int]


class Kind(str, Enum):
    """Negotiation messages followed by boarding and alighting notifications."""
    CFP = "CFP"
    OFFER = "OFFER"
    ACCEPT = "ACCEPT"
    CONFIRM = "CONFIRM"
    REJECT = "REJECT"
    CLOSE = "CLOSE"
    BOARD_START = "BOARD_START"
    BOARD_END = "BOARD_END"
    DROP_START = "DROP_START"
    DROP_END = "DROP_END"


@dataclass(frozen=True)
class Message:
    """An addressed envelope; tick records when it was sent, not a delay."""
    sender: Address
    recipient: Address
    kind: Kind
    tick: int
    payload: object


class MessageBus:
    """Each send delivers one envelope to one recipient's independent queue.

    Callers broadcast by sending to every address. Envelopes are distinct;
    immutable payloads can be shared without copying their contents. Agents
    consume only their own inbox. The optional log is for observation.
    """

    def __init__(self, trace=False):
        # Each address gets its own FIFO queue, created on first access.
        self._inboxes = defaultdict(deque)
        self.trace = trace
        self.history = []
        # Count deliveries, not broadcasts: one CFP to eight taxis counts eight.
        self.counts = Counter()

    def send(self, sender, recipient, kind, tick, payload):
        """Enqueue immediately; model phases determine when it is consumed."""
        message = Message(sender, recipient, kind, tick, payload)
        self._inboxes[recipient].append(message)
        self.counts[kind.value] += 1
        if self.trace:
            # Consuming an inbox message does not remove it from the audit log.
            self.history.append(message)

    def receive(self, address, kinds):
        """Consume matching messages once, preserving order in both groups.

        For example, receiving OFFER leaves a queued CONFIRM untouched. This
        lets negotiation and transport share an inbox without stealing events
        from one another. It does not validate or accept an offer by itself.
        """
        inbox = self._inboxes[address]
        selected, remaining = [], deque()
        while inbox:
            message = inbox.popleft()
            # Receiving offers must not accidentally consume a confirmation or
            # transport event intended for a later phase of the same tick.
            (selected if message.kind in kinds else remaining).append(message)
        self._inboxes[address] = remaining
        return selected

    def empty(self):
        """Check pending inboxes; counters and recorded history are not queues."""
        return not any(self._inboxes.values())
