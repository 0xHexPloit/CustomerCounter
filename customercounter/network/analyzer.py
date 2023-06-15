from typing import Tuple

from mac_vendor_lookup import MacLookup
from scapy.all import Packet

from customercounter.operating_system import OperatingSystem


def get_constructor(macAddr: str):
    try:
        return MacLookup().lookup(macAddr)
    except KeyError:
        return ""


def analyze(packet: Packet) -> Tuple[str, str, OperatingSystem]:
    mac_src = packet.addr2
    NIC = mac_src[9:]
    constr = get_constructor(mac_src)

    if "Apple" in constr:
        return mac_src, NIC, OperatingSystem.APPLE
    elif len(constr) == 0:
        return mac_src, NIC, OperatingSystem.OTHER
    else:
        return mac_src, NIC, OperatingSystem.ANDROID
