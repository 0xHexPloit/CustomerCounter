from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    device_id: str
    vendor: str
