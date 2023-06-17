import threading
from abc import ABC, abstractmethod
from typing import Optional


class IThreadManager(ABC):
    @abstractmethod
    def spawn(self):
        raise NotImplementedError()

    @abstractmethod
    def terminate(self):
        raise NotImplementedError()

    @abstractmethod
    def get_thread(self) -> Optional[threading.Thread]:
        raise NotImplementedError()
