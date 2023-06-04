import pytest

from customercounter.event.event import Event


@pytest.fixture
def event():
    default_event = Event("AE-B4-C5", "Apple")
    return default_event
