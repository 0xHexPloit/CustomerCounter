from confz import ConfZ, ConfZFileSource
from pydantic import validator
from pathlib import Path


class StateMachineSettings(ConfZ):
    attempts_in_potential_leaving: int
    
    @validator("attempts_in_potential_leaving")
    def check_number_attempts_is_positive(cls, v):
        if v < 0:
            raise ValueError("Number of attempts should be positive")
        return v
    

class AppSettings(ConfZ):
    state_machine: StateMachineSettings
    
    CONFIG_SOURCES = ConfZFileSource(file=Path(__file__).parent.parent / "config.yaml")
    

def get_app_settings() -> AppSettings:
    return AppSettings()
