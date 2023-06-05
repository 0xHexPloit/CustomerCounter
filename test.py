import threading
import time
from typing import List

import pytermgui as ptg

from customercounter.electronic_device.store import IElectronicDevicesStoreUpdateSubscriber, ElectronicDevicesStore
from customercounter.event import Event
from customercounter.event.manager import EventManager
from customercounter.event.receiver import IEventReceiver
from customercounter.electronic_device.state_machine import ElectronicDevicePresenceMachineState

from loguru import logger

from threading import Lock, Thread

class FakeEventReceiver(IEventReceiver):
    def __init__(self, events: List[Event]) -> None:
        self.__channel = [events]
        self.__lock = Lock()

    def fill_channel(self, events: List[Event]):
        self.__lock.acquire()
        self.__channel.append(events)
        self.__lock.release()

    def get_events(self) -> List[Event]:
        while len(self.__channel) == 0:
            time.sleep(2)
        self.__lock.acquire()
        events = self.__channel[0]
        self.__channel.pop(0)
        self.__lock.release()
        return events


if __name__ == "__main__":
    label = ptg.Label("Nombre appareils connectés: 0")

    logger.add("./logs.txt")

    def tui_controller_func(label: ptg.Label, store: ElectronicDevicesStore):
        class TUIControllerSubscriber(IElectronicDevicesStoreUpdateSubscriber):
            def handle_store_update(self):
                electronic_devices = store.get_electronic_devices()
                connected_devices = 0

                for device in electronic_devices:
                    if device.get_current_state() == ElectronicDevicePresenceMachineState.POTENTIAL_ARRIVAL:
                        connected_devices += 1

                logger.info("I have been called successfully")

                label.value = f"Nombre appareils connectés: {connected_devices}"

        return TUIControllerSubscriber()

    store = ElectronicDevicesStore()
    event_one = Event("AA-2B-7D", "Apple")
    event_two = Event("AF-12-A3", "Samsung")
    event_receiver = FakeEventReceiver([event_one, event_two])
    tui_controller = tui_controller_func(label, store)

    event_manager = EventManager(store, event_receiver)
    event_manager.add_subscriber(tui_controller)

    def start_event_manager(event_manager: EventManager):
        time.sleep(5)
        event_manager.spawn()


    thread = threading.Thread(target=start_event_manager, args=(event_manager,))
    thread.daemon = True
    thread.start()

    with ptg.WindowManager() as manager:
        window = (
            ptg.Window(
                "",
                label,
                "",
                width=60,
                box="DOUBLE",
            )
            .set_title("[210 bold]New contact")
            .center()
        )

        manager.add(window)
