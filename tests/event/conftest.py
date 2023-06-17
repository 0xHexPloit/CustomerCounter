import pytest

from customercounter.event.event import Event
from customercounter.operating_system import OperatingSystem


@pytest.fixture
def event():
    default_event = Event("AE-A6-B2", OperatingSystem.APPLE)
    return default_event
