from datetime import datetime
from io import StringIO

from loguru import logger

from customercounter.electronic_device.electronic_device import ElectronicDevice
from customercounter.electronic_device.state_machine import (
    ElectronicDevicePresenceMachineState,
)
from customercounter.event.type import EventType
from customercounter.settings import get_app_settings

DEFAULT_DEVICE_ID: str = "A5-26-DC"
DEFAULT_VENDOR: str = "Apple"


def test_should_get_correct_id():
    device = ElectronicDevice(DEFAULT_DEVICE_ID, "")

    assert device.get_id() == DEFAULT_DEVICE_ID


def test_should_get_correct_vendor_name():
    device = ElectronicDevice("", DEFAULT_VENDOR)

    assert device.get_vendor() == DEFAULT_VENDOR


def test_should_get_correct_initial_state():
    device = ElectronicDevice("", "")
    assert (
        device.get_current_state()
        == ElectronicDevicePresenceMachineState.POTENTIAL_ARRIVAL
    )


def test_should_move_to_in_mall_state_when_dealing_with_received_probe_request_event():
    device = ElectronicDevice("", "")
    device.update_device_state(EventType.PROBE_REQUEST_RECEIVED)
    new_state = device.get_current_state()

    assert new_state == ElectronicDevicePresenceMachineState.IN_MALL


def test_should_move_to_false_positive_when_dealing_with_no_probe_request_received_event():
    device = ElectronicDevice("", "")
    device.update_device_state(EventType.NO_PROBE_REQUEST_RECEIVED)
    new_state = device.get_current_state()

    assert new_state == ElectronicDevicePresenceMachineState.FALSE_POSITIVE


def test_should_log_state_transition_when_moving_from_one_state_to_another():
    buffer = StringIO()
    handle_id = logger.add(buffer)

    device = ElectronicDevice(DEFAULT_DEVICE_ID, DEFAULT_VENDOR)
    device.update_device_state(EventType.PROBE_REQUEST_RECEIVED)

    log = buffer.getvalue().strip("\n")
    log_items = log.split("|")[2:]

    # Checking the number of items
    assert len(log_items) == 4

    assert log_items[0].split(" - ")[1].strip() == DEFAULT_DEVICE_ID
    assert log_items[1].strip() == DEFAULT_VENDOR

    # Retrieving machine states
    states = log_items[2].split("-->")
    old_state = ElectronicDevicePresenceMachineState.parse_from_raw(states[0].strip())
    new_state = ElectronicDevicePresenceMachineState.parse_from_raw(states[1].strip())

    assert old_state == ElectronicDevicePresenceMachineState.POTENTIAL_ARRIVAL
    assert new_state == ElectronicDevicePresenceMachineState.IN_MALL

    # Trying parsing timestamp
    datetime.strptime(log_items[3].strip(), "%Y-%m-%d %H:%M:%S.%f")

    logger.remove(handle_id)


def test_should_not_log_state_transition_if_staying_in_same_state():
    buffer = StringIO()
    handle_id = logger.add(buffer)

    device = ElectronicDevice("", "")
    device.update_device_state(EventType.PROBE_REQUEST_RECEIVED)
    device.update_device_state(EventType.PROBE_REQUEST_RECEIVED)

    logs = [item for item in buffer.getvalue().split("\n") if item != ""]

    assert len(logs) == 1

    logger.remove(handle_id)


def test_should_get_a_timestamp_when_moving_from_potential_arrival_to_in_mall():
    device = ElectronicDevice("", "")
    device.update_device_state(EventType.PROBE_REQUEST_RECEIVED)
    timestamps = device.get_in_mall_timestamps()

    assert len(timestamps) == 1


def test_should_get_a_timestamp_when_moving_from_potential_leaving_to_left():
    device = ElectronicDevice("", "")
    device.update_device_state(EventType.PROBE_REQUEST_RECEIVED)

    settings = get_app_settings()

    for i in range(settings.smachine.plattempts + 2):
        device.update_device_state(EventType.NO_PROBE_REQUEST_RECEIVED)

    timestamps = device.get_left_timestamps()

    assert len(timestamps) == 1
