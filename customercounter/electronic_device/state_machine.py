from statemachine import State, StateMachine

from customercounter.settings import get_app_settings


class ElectronicDevicePresenceMachine(StateMachine):
    potential_arrival = State(initial=True)
    in_mall = State()
    false_positive = State()
    potential_leaving = State()
    left = State()

    probe_request_received = (
        potential_arrival.to(in_mall)
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
        | potential_leaving.to(left)
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

    def get_remaining_potential_leaving_attempts(self) -> int:
        return self.__number_attempts_in_potential_leaving
