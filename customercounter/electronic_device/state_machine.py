import typing
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

from statemachine import State, StateMachine

from customercounter.settings import get_app_settings


class ElectronicDevicePresenceMachineState(Enum):
    POTENTIAL_ARRIVAL = "POTENTIAL_ARRIVAL"
    IN_MALL = "IN_MALL"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    POTENTIAL_LEAVING = "POTENTIAL_LEAVING"
    LEFT = "LEFT"

    @staticmethod
    def parse_from_raw(value: str) -> "ElectronicDevicePresenceMachineState":
        upper_value = value.upper()

        if upper_value == ElectronicDevicePresenceMachineState.POTENTIAL_ARRIVAL.value:
            return ElectronicDevicePresenceMachineState.POTENTIAL_ARRIVAL
        elif upper_value == ElectronicDevicePresenceMachineState.IN_MALL.value:
            return ElectronicDevicePresenceMachineState.IN_MALL
        elif upper_value == ElectronicDevicePresenceMachineState.FALSE_POSITIVE.value:
            return ElectronicDevicePresenceMachineState.FALSE_POSITIVE
        elif (
            upper_value == ElectronicDevicePresenceMachineState.POTENTIAL_LEAVING.value
        ):
            return ElectronicDevicePresenceMachineState.POTENTIAL_LEAVING
        elif upper_value == ElectronicDevicePresenceMachineState.LEFT.value:
            return ElectronicDevicePresenceMachineState.LEFT
        else:
            raise ValueError("Invalid entry for ElectronicDevicePresenceMachineState!")


class IElectronicDevicePresenceMachine(typing.Protocol):
    def get_in_mall_timestamps(self) -> typing.List[datetime]:
        ...

    def get_left_timestamps(self) -> typing.List[datetime]:
        ...

    def get_remaining_potential_leaving_attempts(self) -> int:
        ...

    def probe_request_received(self):
        ...

    def no_probe_request_received(self):
        ...

    def get_current_state(self) -> ElectronicDevicePresenceMachineState:
        ...


class ElectronicDevicePresenceMachine(StateMachine):
    potential_arrival = State(initial=True)
    in_mall = State()
    false_positive = State()
    potential_leaving = State()
    left = State()

    probe_request_received = (
        potential_arrival.to(in_mall, on="_add_in_mall_timestamp")
        | potential_leaving.to(
            in_mall, on="_reset_remaining_potential_leaving_attempts"
        )
        | left.to(potential_arrival, on="_reset_remaining_potential_leaving_attempts")
        | false_positive.to(potential_arrival)
        | in_mall.to(in_mall)
    )

    no_probe_request_received = (
        potential_arrival.to(false_positive)
        | in_mall.to(potential_leaving)
        | potential_leaving.to(
            potential_leaving, cond="_potential_leaving_attempts_still_positive"
        )
        | potential_leaving.to(left, on="_add_left_timestamp")
        | left.to(left)
        | false_positive.to(false_positive)
    )

    def __init__(self, number_attempts_in_potential_leaving: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_number_attempts_in_potential_leaving = (
            number_attempts_in_potential_leaving
        )
        self.__number_attempts_in_potential_leaving = (
            number_attempts_in_potential_leaving
        )
        self.__in_mall_timestamps: typing.List[datetime] = []
        self.__left_timestamps: typing.List[datetime] = []

    @staticmethod
    def build_default_machine() -> "ElectronicDevicePresenceMachine":
        settings = get_app_settings()
        return ElectronicDevicePresenceMachine(
            settings.state_machine.attempts_in_potential_leaving
        )

    def _potential_leaving_attempts_still_positive(self):
        should_move_to_left_state = self.__number_attempts_in_potential_leaving != 0
        if self.__number_attempts_in_potential_leaving > 0:
            self.__number_attempts_in_potential_leaving -= 1
        return should_move_to_left_state

    def _reset_remaining_potential_leaving_attempts(self):
        self.__number_attempts_in_potential_leaving = (
            self.__initial_number_attempts_in_potential_leaving
        )

    def _add_in_mall_timestamp(self):
        self.__in_mall_timestamps.append(datetime.now())

    def _add_left_timestamp(self):
        self.__left_timestamps.append(datetime.now())

    def get_in_mall_timestamps(self) -> typing.List[datetime]:
        return self.__in_mall_timestamps

    def get_left_timestamps(self) -> typing.List[datetime]:
        return self.__left_timestamps

    def get_remaining_potential_leaving_attempts(self) -> int:
        return self.__number_attempts_in_potential_leaving

    def get_current_state(self) -> ElectronicDevicePresenceMachineState:
        return ElectronicDevicePresenceMachineState.parse_from_raw(
            self.current_state.id
        )
