from enum import Enum, auto


class EventType(Enum):
    EVENT_RECEIVED = auto()
    NO_EVENT_RECEIVED = auto()
