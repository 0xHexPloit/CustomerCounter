import sys
import time
from multiprocessing import Lock
from typing import List

from customercounter.event.event import Event
from customercounter.event.receiver import IEventReceiver
from customercounter.tui import CustomerCounterTUI
from customercounter.electronic_device.store import ElectronicDevicesStore
from customercounter.event.manager import EventManager
from customercounter.operating_system import OperatingSystem
class FakeEventReceiver(IEventReceiver):
    def __init__(self, events: List[Event]) -> None:
        self.__channel = [events]
        self.__lock = Lock()

    def fill_channel(self, events: List[Event]):
        self.__lock.acquire()
        self.__channel.append(events)
        self.__lock.release()

    def get_events(self) -> List[Event]:
        time.sleep(2)
        while len(self.__channel) == 0:
            time.sleep(2)
        self.__lock.acquire()
        events = self.__channel[0]
        self.__channel.pop(0)
        self.__lock.release()

        return events


if __name__ == "__main__":
    events = [
        Event(device_id="22-13-28", os=OperatingSystem.APPLE),
        Event(device_id="24-27-23", os=OperatingSystem.ANDROID),
        Event(device_id="2E-A1-4F", os=OperatingSystem.OTHER)
    ]
    import loguru

    loguru.logger.remove()

    event_receiver = FakeEventReceiver([])
    event_receiver.fill_channel(events)
    event_receiver.fill_channel(events)

    for i in range(20):
        event_receiver.fill_channel([])

    store = ElectronicDevicesStore.get_instance()
    event_manager = EventManager(store, event_receiver)

    tui = CustomerCounterTUI(event_manager)

    tui.run()