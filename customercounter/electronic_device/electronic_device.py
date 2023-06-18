import typing
from abc import ABC, abstractmethod
from datetime import datetime

from loguru import logger

from customercounter.electronic_device.state_machine import (
    ElectronicDevicePresenceMachine,
    ElectronicDevicePresenceMachineState,
    IElectronicDevicePresenceMachine,
)
from customercounter.event.type import EventType
from customercounter.operating_system import OperatingSystem


class IElectronicDevice(ABC):
    @abstractmethod
    def get_id(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_os(self) -> OperatingSystem:
        raise NotImplementedError()

    @abstractmethod
    def change_os(self, new_os: OperatingSystem):
        raise NotImplementedError()

    @abstractmethod
    def get_current_state(self) -> ElectronicDevicePresenceMachineState:
        raise NotImplementedError()

    @abstractmethod
    def update_device_state(self, event_type: EventType):
        raise NotImplementedError()

    @abstractmethod
    def get_in_mall_timestamps(self) -> typing.List[datetime]:
        raise NotImplementedError()

    @abstractmethod
    def get_left_timestamps(self) -> typing.List[datetime]:
        raise NotImplementedError()


class ElectronicDevice(IElectronicDevice):
    def __init__(self, device_id: str, os: OperatingSystem):
        self.__id = device_id
        self.__os = os
        self.__state: IElectronicDevicePresenceMachine = (
            ElectronicDevicePresenceMachine.build_default_machine()
        )

    def get_id(self) -> str:
        return self.__id

    def get_os(self) -> OperatingSystem:
        return self.__os

    def change_os(self, new_os: OperatingSystem):
        self.__os = new_os

    def get_current_state(self) -> ElectronicDevicePresenceMachineState:
        return self.__state.get_current_state()

    def update_device_state(self, event_type: EventType):
        old_state = self.get_current_state()

        if event_type == EventType.EVENT_RECEIVED:
            self.__state.event_received()
        else:
            self.__state.no_event_received()

        new_state = self.get_current_state()

        if old_state != new_state:
            self._log_transition(old_state, new_state)

    def _log_transition(
        self,
        old_state: ElectronicDevicePresenceMachineState,
        new_state: ElectronicDevicePresenceMachineState,
    ):
        current_timestamp = datetime.now()
        logger.info(
            f"{self.__id} | {self.__os.value} | {old_state.value} --> {new_state.value} | {current_timestamp}"
        )

    def get_in_mall_timestamps(self) -> typing.List[datetime]:
        return self.__state.get_in_mall_timestamps()

    def get_left_timestamps(self) -> typing.List[datetime]:
        return self.__state.get_left_timestamps()
