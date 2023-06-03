from enum import Enum, auto


class EventType(Enum):
    PROBE_REQUEST_RECEIVED = auto()
    NO_PROBE_REQUEST_RECEIVED = auto()
