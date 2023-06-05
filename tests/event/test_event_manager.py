import time
from threading import Lock
from typing import List

from customercounter.electronic_device.state_machine import (
    ElectronicDevicePresenceMachineState,
)
from customercounter.electronic_device.store import (
    ElectronicDevicesStore,
    IElectronicDevicesStoreUpdateSubscriber,
)
from customercounter.event.event import Event
from customercounter.event.manager import EventManager
from customercounter.event.receiver import IEventReceiver


class FakeStoreSubscriber(IElectronicDevicesStoreUpdateSubscriber):
    def __init__(self) -> None:
        self.__handle_func_called = False

    def does_handle_func_called(self) -> bool:
        return self.__handle_func_called

    def handle_store_update(self):
        self.__handle_func_called = True


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


def test_should_notify_subscribers_about_store_changes(event):
    store = ElectronicDevicesStore()
    events_receiver = FakeEventReceiver([event])
    subscriber = FakeStoreSubscriber()
    event_manager = EventManager(store, events_receiver)
    event_manager.add_subscriber(subscriber)
    event_manager.spawn()
    time.sleep(1)
    event_manager.terminate()

    assert subscriber.does_handle_func_called() == True


def test_should_add_event_in_store_if_it_is_not_already_stored(event):
    store = ElectronicDevicesStore()
    events_receiver = FakeEventReceiver([event])
    event_manager = EventManager(store, events_receiver)
    event_manager.spawn()
    time.sleep(1)
    event_manager.terminate()

    store_size = len(store.get_electronic_devices())
    assert store_size == 1


def test_should_send_probe_request_received_event_if_device_id_is_in_event_channel(
    event: Event,
):
    store = ElectronicDevicesStore()
    events_receiver = FakeEventReceiver([event])
    events_receiver.fill_channel([event])
    event_manager = EventManager(store, events_receiver)
    event_manager.spawn()
    time.sleep(1)
    event_manager.terminate()

    device = store.get_electronic_device(event.device_id)
    device_state = device.get_current_state()

    assert device_state == ElectronicDevicePresenceMachineState.IN_MALL


def test_should_no_probe_request_received_event_id_device_id_is_not_in_event_channel(
    event: Event,
):
    store = ElectronicDevicesStore()
    events_receiver = FakeEventReceiver([event])
    events_receiver.fill_channel([])
    event_manager = EventManager(store, events_receiver)
    event_manager.spawn()
    time.sleep(1)
    event_manager.terminate()

    device = store.get_electronic_device(event.device_id)
    device_state = device.get_current_state()

    assert device_state == ElectronicDevicePresenceMachineState.FALSE_POSITIVE
