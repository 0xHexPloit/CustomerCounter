from customercounter.electronic_device.state_machine import (
    ElectronicDevicePresenceMachine,
)
from customercounter.settings import get_app_settings


def test_initial_state_is_potential_arrival():
    machine = ElectronicDevicePresenceMachine.build_default_machine()
    assert machine.current_state.id == "potential_arrival"


def test_move_from_potential_arrival_to_in_mall_on_probe_request_received():
    machine = ElectronicDevicePresenceMachine.build_default_machine()
    machine.send("probe_request_received")
    assert machine.current_state.id == "in_mall"


def test_move_from_potential_arrival_to_false_positive_if_receiving_no_probe_request():
    machine = ElectronicDevicePresenceMachine.build_default_machine()
    machine.send("no_probe_request_received")
    assert machine.current_state.id == "false_positive"


def test_move_from_in_mall_to_potential_leaving_if_receiving_no_probe_request():
    machine = ElectronicDevicePresenceMachine.build_default_machine()
    machine.probe_request_received()
    machine.no_probe_request_received()
    assert machine.current_state.id == "potential_leaving"


def test_should_return_to_in_mall_from_potential_leaving_if_receiving_probe_request():
    machine = ElectronicDevicePresenceMachine.build_default_machine()
    machine.probe_request_received()
    machine.no_probe_request_received()
    machine.probe_request_received()
    assert machine.current_state.id == "in_mall"


def test_should_stay_in_potential_leaving_on_no_probe_request_received_if_number_attempts_still_positive():
    machine = ElectronicDevicePresenceMachine.build_default_machine()
    machine.probe_request_received()
    machine.no_probe_request_received()
    machine.no_probe_request_received()

    assert machine.current_state.id == "potential_leaving"


def test_should_move_from_potential_leaving_to_left_if_no_probe_request_received_and_no_more_attempts_possible():
    machine = ElectronicDevicePresenceMachine(number_attempts_in_potential_leaving=0)
    machine.probe_request_received()
    machine.no_probe_request_received()
    machine.no_probe_request_received()

    assert machine.current_state.id == "left"


def test_should_decrement_number_attempts_when_receiving_no_probe_request_on_potential_leaving_state():
    machine = ElectronicDevicePresenceMachine.build_default_machine()
    machine.probe_request_received()
    machine.no_probe_request_received()
    machine.no_probe_request_received()

    settings = get_app_settings()

    remaining_attempts = machine.get_remaining_potential_leaving_attempts()

    assert remaining_attempts == settings.smachine.plattempts - 1


def test_should_move_from_left_to_potential_arrival_when_receiving_probe_request():
    machine = ElectronicDevicePresenceMachine(0)
    machine.probe_request_received()
    machine.no_probe_request_received()
    machine.no_probe_request_received()
    machine.probe_request_received()

    assert machine.current_state.id == "potential_arrival"


def test_should_move_from_false_positive_to_potential_arrival_when_receiving_probe_requests():
    machine = ElectronicDevicePresenceMachine.build_default_machine()
    machine.no_probe_request_received()
    machine.probe_request_received()

    assert machine.current_state.id == "potential_arrival"


def test_should_reset_remaining_potential_leaving_attempts_when_moving_from_potential_leaving_to_in_mall():
    machine = ElectronicDevicePresenceMachine.build_default_machine()
    machine.probe_request_received()
    machine.no_probe_request_received()
    machine.no_probe_request_received()
    machine.probe_request_received()

    settings = get_app_settings()
    remaining_attempts = machine.get_remaining_potential_leaving_attempts()

    assert remaining_attempts == settings.smachine.plattempts


def test_should_reset_remaining_potential_leaving_attemps_when_moving_from_left_to_potential_arrival():
    number_attempts_allowed = 0
    machine = ElectronicDevicePresenceMachine(number_attempts_allowed)
    machine.probe_request_received()
    machine.no_probe_request_received()
    machine.no_probe_request_received()
    machine.probe_request_received()

    remaining_attempts = machine.get_remaining_potential_leaving_attempts()

    assert remaining_attempts == number_attempts_allowed


def test_should_stay_in_mall_when_receiving_probe_request():
    machine = ElectronicDevicePresenceMachine.build_default_machine()
    machine.probe_request_received()
    machine.probe_request_received()

    assert machine.current_state.id == "in_mall"


def test_should_stay_in_left_when_receiving_no_probe_request():
    machine = ElectronicDevicePresenceMachine(0)
    machine.probe_request_received()
    machine.no_probe_request_received()
    machine.no_probe_request_received()
    machine.no_probe_request_received()

    assert machine.current_state.id == "left"


def test_should_stay_in_false_positive_when_receiving_no_probe_request():
    machine = ElectronicDevicePresenceMachine.build_default_machine()
    machine.no_probe_request_received()
    machine.no_probe_request_received()

    assert machine.current_state.id == "false_positive"


def test_should_add_timestamp_when_moving_from_potential_arrival_to_in_mall():
    machine = ElectronicDevicePresenceMachine.build_default_machine()
    machine.probe_request_received()
    timestamps = machine.get_in_mall_timestamps()

    assert len(timestamps) == 1


def test_should_add_timestamp_when_moving_from_potential_leaving_to_left():
    machine = ElectronicDevicePresenceMachine(0)
    machine.probe_request_received()
    machine.no_probe_request_received()
    machine.no_probe_request_received()
    timestamps = machine.get_left_timestamps()

    assert len(timestamps) == 1
