from abc import ABC, abstractmethod
from multiprocessing.connection import Connection
from typing import List

from customercounter.event.event import Event


class IEventTransmitter(ABC):
    @abstractmethod
    def send(self, events: List[Event]):
        raise NotImplementedError()


class PipeEventTransmitter(IEventTransmitter):
    def __init__(self, tx: Connection) -> None:
        self.__tx = tx

    def send(self, events: List[Event]):
        self.__tx.send(events)
