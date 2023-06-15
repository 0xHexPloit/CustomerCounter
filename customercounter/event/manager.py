import threading
import typing

from customercounter.electronic_device.electronic_device import (
    ElectronicDevice,
    IElectronicDevice,
)
from customercounter.electronic_device.store import (
    IElectronicDevicesStore,
    IElectronicDevicesStoreUpdateNotifier,
    IElectronicDevicesStoreUpdateSubscriber,
)
from customercounter.event.receiver import IEventReceiver
from customercounter.event.type import EventType
from customercounter.thread import IThreadManager


class IEventManager(IThreadManager, IElectronicDevicesStoreUpdateNotifier):
    ...


def thread_func(
    store: IElectronicDevicesStore,
    receiver: IEventReceiver,
    store_update_delegate: IElectronicDevicesStoreUpdateNotifier,
    should_exit: typing.Callable[[], bool],
):
    while not should_exit():
        # Receiving events from event channel
        received_events = receiver.get_events()

        # Keep track of events that have been processed
        seen_devices: typing.Set[IElectronicDevice] = set()

        for event in received_events:
            # Checking if the electronic device is already stored in the store. If not add it to the store
            device = store.get_electronic_device(event.device_id)

            if device is None:
                new_device = ElectronicDevice(event.device_id, event.os)
                store.add_electronic_device(new_device)
                seen_devices.add(new_device)
            else:
                # If device already exists, we simply need to update its state
                device.update_device_state(EventType.PROBE_REQUEST_RECEIVED)
                seen_devices.add(device)

        # Next step we should retrieve all the devices that we have not seen previously and update their state
        all_devices_in_storage: typing.Set[IElectronicDevice] = set(
            store.get_electronic_devices()
        )
        not_seen_devices = all_devices_in_storage.difference(seen_devices)

        for device in not_seen_devices:
            device.update_device_state(EventType.NO_PROBE_REQUEST_RECEIVED)

        # Notifying about store changes
        store_update_delegate.notify_store_update()


class EventManager(IEventManager, IElectronicDevicesStoreUpdateNotifier):
    def __init__(
        self, store: IElectronicDevicesStore, receiver: IEventReceiver
    ) -> None:
        self.__store = store
        self.__receiver = receiver
        self.__thread: typing.Optional[threading.Thread] = None
        self.__subscribers: typing.List[IElectronicDevicesStoreUpdateSubscriber] = []
        self.__should_exit = False

    def spawn(self):
        self.__thread = threading.Thread(
            target=thread_func,
            args=(self.__store, self.__receiver, self, lambda: self.__should_exit),
        )
        self.__thread.daemon = True
        self.__thread.start()

    def terminate(self):
        self.__should_exit = True

    def notify_store_update(self):
        for subscriber in self.__subscribers:
            subscriber.handle_store_update()

    def add_subscriber(self, subscriber: IElectronicDevicesStoreUpdateSubscriber):
        self.__subscribers.append(subscriber)

    def get_thread(self) -> typing.Optional[threading.Thread]:
        return self.__thread
