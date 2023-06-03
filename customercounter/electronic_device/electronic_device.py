from abc import ABC, abstractmethod
from datetime import datetime

from loguru import logger

from customercounter.electronic_device.state_machine import (
    ElectronicDevicePresenceMachine,
    ElectronicDevicePresenceMachineState,
)
from customercounter.event.type import EventType


class IElectronicDevice(ABC):
    @abstractmethod
    def get_id(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_vendor(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def get_current_state(self) -> ElectronicDevicePresenceMachineState:
        raise NotImplementedError()

    @abstractmethod
    def update_device_state(self, event_type: EventType):
        raise NotImplementedError()


class ElectronicDevice(IElectronicDevice):
    def __init__(self, device_id: str, vendor: str):
        self.__id = device_id
        self.__vendor = vendor
        self.__state = ElectronicDevicePresenceMachine.build_default_machine()

    def get_id(self) -> str:
        return self.__id

    def get_vendor(self) -> str:
        return self.__vendor

    def get_current_state(self) -> ElectronicDevicePresenceMachineState:
        return ElectronicDevicePresenceMachineState.parse_from_raw(
            self.__state.current_state.id
        )

    def update_device_state(self, event_type: EventType):
        old_state = self.get_current_state()

        if event_type == EventType.PROBE_REQUEST_RECEIVED:
            self.__state.probe_request_received()
        else:
            self.__state.no_probe_request_received()

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
            f"{self.__id} | {self.__vendor} | {old_state.value} --> {new_state.value} | {current_timestamp}"
        )
