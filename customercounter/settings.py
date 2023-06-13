# mypy: disable-error-code="misc"
from pathlib import Path

from confz import ConfZ, ConfZEnvSource, ConfZFileSource
from pydantic import validator


class StateMachineSettings(ConfZ):
    plattempts: int

    @validator("plattempts")
    def check_number_attempts_is_positive(cls, v):
        if v < 0:
            raise ValueError("Number of attempts should be positive")
        return v


class EventsCollectorSettings(ConfZ):
    interval: int

    @validator("interval")
    def check_collect_time_interval_is_positive(cls, v):
        if v < 0:
            raise ValueError("Collect time interval should be positive")
        return v


class AppSettings(ConfZ):
    smachine: StateMachineSettings
    collector: EventsCollectorSettings

    CONFIG_SOURCES = [
        ConfZFileSource(file=Path(__file__).parent.parent / "config.yaml"),
        ConfZEnvSource(prefix="CCOUNTER_", allow_all=True, nested_separator="_"),
    ]


def get_app_settings() -> AppSettings:
    return AppSettings()
