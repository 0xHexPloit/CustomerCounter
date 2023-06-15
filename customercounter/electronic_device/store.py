import typing
from abc import ABC, abstractmethod
from typing import Protocol

from customercounter.electronic_device.electronic_device import IElectronicDevice


class IElectronicDevicesStoreUpdateSubscriber(Protocol):
    def handle_store_update(self):
        raise NotImplementedError()


class IElectronicDevicesStoreUpdateNotifier(ABC):
    @abstractmethod
    def notify_store_update(self):
        raise NotImplementedError()

    @abstractmethod
    def add_subscriber(self, subscriber: IElectronicDevicesStoreUpdateSubscriber):
        raise NotImplementedError()


class IElectronicDevicesStore(ABC):
    @abstractmethod
    def get_electronic_devices(self) -> typing.List[IElectronicDevice]:
        raise NotImplementedError()

    @abstractmethod
    def get_electronic_device(
        self, device_id: str
    ) -> typing.Optional[IElectronicDevice]:
        raise NotImplementedError()

    @abstractmethod
    def add_electronic_device(self, device: IElectronicDevice):
        raise NotImplementedError()

    @abstractmethod
    def clear_storage(self):
        raise NotImplementedError()

    @abstractmethod
    def get_instance(self) -> "IElectronicDevicesStore":
        raise NotImplementedError()


class ElectronicDevicesStore(IElectronicDevicesStore):
    _instance: typing.Optional["ElectronicDevicesStore"] = None

    def __init__(self):
        self.__devices: typing.Dict[str, IElectronicDevice] = {}

    def get_electronic_devices(self) -> typing.List[IElectronicDevice]:
        return list(self.__devices.values())

    def get_electronic_device(
        self, device_id: str
    ) -> typing.Optional[IElectronicDevice]:
        return self.__devices.get(device_id)

    def add_electronic_device(self, device: IElectronicDevice):
        device_id = device.get_id()
        self.__devices[device_id] = device

    def clear_storage(self):
        self.__devices = {}

    @classmethod
    def get_instance(cls) -> "IElectronicDevicesStore":
        if cls._instance is None:
            cls._instance = ElectronicDevicesStore()
        return cls._instance
