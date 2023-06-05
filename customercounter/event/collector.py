import threading
import time
import typing
from typing import Any

from customercounter.event.pool import IEventPool
from customercounter.event.transmitter import IEventTransmitter
from customercounter.thread import IThreadManager


class IEventCollector(IThreadManager):
    ...


def thread_func(
    pool: IEventPool,
    transmitter: IEventTransmitter,
    sleeping_duration: int,
    should_exit: typing.Callable[[], bool],
):
    while not should_exit():
        events = pool.remove_all_events()
        transmitter.send(events)
        time.sleep(sleeping_duration)


class EventCollector(IEventCollector):
    def __init__(
        self, pool: IEventPool, transmitter: IEventTransmitter, sleeping_duration: int
    ) -> None:
        self.__pool = pool
        self.__transmitter = transmitter
        self.__sleeping_duration = sleeping_duration
        self.__should_exit = False
        self.__thread: typing.Optional[threading.Thread] = None

    def spawn(self):
        self.__thread = threading.Thread(
            target=thread_func,
            args=(
                self.__pool,
                self.__transmitter,
                self.__sleeping_duration,
                lambda: self.__should_exit,
            ),
        )
        self.__thread.daemon = True
        self.__thread.start()

    def terminate(self):
        self.__should_exit = True

    def get_thread(self) -> typing.Optional[threading.Thread]:
        return self.__thread
