from dataclasses import dataclass

from customercounter.operating_system import OperatingSystem


@dataclass(frozen=True)
class Event:
    device_id: str
    os: OperatingSystem
