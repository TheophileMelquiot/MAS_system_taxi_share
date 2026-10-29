"""Addressed mailboxes: transport messages, never make allocation decisions."""

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from enum import Enum

Address = tuple[str, int]


class Kind(str, Enum):
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
    sender: Address
    recipient: Address
    kind: Kind
    tick: int
    payload: object


class MessageBus:
    """A broadcast delivers separate copies to independent recipient queues.

    Agents consume only their own inbox. The optional audit log is for the
    observer, never a source of knowledge for a taxi or passenger.
    """

    def __init__(self, trace=False):
        self._inboxes = defaultdict(deque)
        self.trace = trace
        self.history = []
        self.counts = Counter()

    def send(self, sender, recipient, kind, tick, payload):
        message = Message(sender, recipient, kind, tick, payload)
        self._inboxes[recipient].append(message)
        self.counts[kind.value] += 1
        if self.trace:
            self.history.append(message)

    def receive(self, address, kinds):
        """Drain selected message types, keeping other phases' messages queued."""
        inbox = self._inboxes[address]
        selected, remaining = [], deque()
        while inbox:
            message = inbox.popleft()
            (selected if message.kind in kinds else remaining).append(message)
        self._inboxes[address] = remaining
        return selected

    def empty(self):
        return not any(self._inboxes.values())
