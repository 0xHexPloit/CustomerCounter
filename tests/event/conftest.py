import pytest

from customercounter.event.event import Event


@pytest.fixture
def event():
    default_event = Event("AE-A6-B2", "Apple")

