import time
from typing import List

from customercounter.event.collector import EventCollector
from customercounter.event.event import Event
from customercounter.event.pool import EventPool
from customercounter.event.transmitter import IEventTransmitter


class FakeEventTransmitter(IEventTransmitter):
    def __init__(self) -> None:
        self.__events: List[Event] = []

    def get_events(self) -> List[Event]:
        # Simulating blocking event until events array becomes not empty
        while True:
            if len(self.__events) != 0:
                return self.__events
            time.sleep(2)

    def send(self, events: List[Event]):
        self.__events = events


def test_event_collector_should_retrieve_events_from_pool_and_transmit_them_using_transmitter(
    event,
):
    transmitter = FakeEventTransmitter()
    pool = EventPool()
    pool.add_event(event)
    collector = EventCollector(
        pool, transmitter, sleeping_duration=60
    )  # Sleep for one minute
    collector.spawn()
    received_events = transmitter.get_events()
    collector.terminate()

    assert len(received_events) == 1
    assert received_events[0] is event
