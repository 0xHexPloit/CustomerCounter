from abc import ABC, abstractmethod
from multiprocessing.connection import Connection
from typing import List

from customercounter.event.event import Event


class IEventReceiver(ABC):
    @abstractmethod
    def get_events(self) -> List[Event]:
        raise NotImplementedError()


class PipeEventReceiver(IEventReceiver):
    def __init__(self, rx: Connection) -> None:
        self.__rx = rx

    def get_events(self) -> List[Event]:
        return self.__rx.recv()
