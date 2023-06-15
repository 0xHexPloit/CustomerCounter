from abc import ABC, abstractmethod
from typing import List, Set


class IMacAddressStore(ABC):
    @abstractmethod
    def add(self, mac_address: str):
        raise NotImplementedError()

    @abstractmethod
    def does_contain(self, mac_address: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_mac_addresses(self) -> List[str]:
        raise NotImplementedError()


class MacAddressStore(IMacAddressStore):
    def __init__(self):
        self.__mac_addresses: Set[str] = set()

    def add(self, mac_address: str):
        self.__mac_addresses.add(mac_address)

    def does_contain(self, mac_address: str) -> bool:
        return mac_address in self.__mac_addresses

    def get_mac_addresses(self) -> List[str]:
        return list(self.__mac_addresses)
