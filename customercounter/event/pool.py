import typing
from abc import ABC, abstractmethod
from multiprocessing import Lock

from customercounter.event.event import Event


class IEventPool(ABC):
    @abstractmethod
    def add_event(self, event: Event):
        raise NotImplementedError()

    @abstractmethod
    def remove_all_events(self) -> typing.List[Event]:
        raise NotImplementedError()

    @abstractmethod
    def get_pool_size(self) -> int:
        raise NotImplementedError()


class EventPool(IEventPool):
    def __init__(self) -> None:
        self.__events: typing.Set[Event] = set()
        self.__lock = Lock()

    def add_event(self, event: Event):
        self.__lock.acquire()
        self.__events.add(event)
        self.__lock.release()

    def remove_all_events(self) -> typing.List[Event]:
        self.__lock.acquire()
        output_events = list(self.__events)
        self.__events.clear()
        self.__lock.release()

        return output_events

    def get_pool_size(self) -> int:
        self.__lock.acquire()
        pool_size = len(self.__events)
        self.__lock.release()
        return pool_size
