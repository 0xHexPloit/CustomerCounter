import multiprocessing
from abc import ABC, abstractmethod

from customercounter.event.receiver import IEventReceiver, PipeEventReceiver
from customercounter.event.transmitter import IEventTransmitter, PipeEventTransmitter


class IEventTransmitterReceiver(ABC):
    @abstractmethod
    def get_transmitter(self) -> IEventTransmitter:
        raise NotImplementedError()

    @abstractmethod
    def get_receiver(self) -> IEventReceiver:
        raise NotImplementedError()


class PipeEventTransmitterReceiver(IEventTransmitterReceiver):
    def __init__(self) -> None:
        rx, tx = multiprocessing.Pipe(duplex=False)
        self.__transmitter = PipeEventTransmitter(tx)
        self.__receiver = PipeEventReceiver(rx)

    def get_transmitter(self) -> IEventTransmitter:
        return self.__transmitter

    def get_receiver(self) -> IEventReceiver:
        return self.__receiver
