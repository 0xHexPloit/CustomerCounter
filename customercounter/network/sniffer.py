from loguru import logger
from scapy.all import Packet, sniff
from scapy.layers.dot11 import Dot11, Dot11ProbeReq

from customercounter.event.event import Event
from customercounter.event.pool import IEventPool
from customercounter.network.analyzer import analyze
from customercounter.network.store import IMacAddressStore, MacAddressStore
from customercounter.operating_system import OperatingSystem


def handle_packet(
    packet: Packet, event_pool: IEventPool, mac_address_storage: IMacAddressStore
):
    if packet.haslayer(Dot11ProbeReq):
        mac_address, NIC, device_os = analyze(packet)
        logger.info(f"Probe request from {mac_address} {NIC} {device_os}")

        # Adding Event to the pool
        event_pool.add_event(Event(NIC, device_os))

        # Registering MAC Address for later use
        mac_address_storage.add(mac_address)
    elif packet.haslayer(Dot11) and packet.type == 1 and packet.subtype == 11:
        # Dealing with RTS packet
        mac_address, NIC, device_os = analyze(packet)
        logger.info(f"RTS from {mac_address} {NIC} {device_os}")

        # Checking if the mac address is randomized
        if device_os == OperatingSystem.OTHER:
            # Determining os from pattern (mac address lookup in storage)
            if mac_address_storage.does_contain(mac_address):
                device_os = OperatingSystem.ANDROID
            else:
                device_os = OperatingSystem.APPLE

        # Adding Event in the pool
        event_pool.add_event(Event(device_id=NIC, os=device_os))


def start_probe_requests_listener(interface: str, event_pool: IEventPool):
    storage = MacAddressStore()

    def handle_packet_wrapper(packet: Packet):
        handle_packet(packet, event_pool, storage)

    logger.info(f"Starting listening for packets on interface: {interface} !")
    sniff(iface=interface, prn=handle_packet_wrapper)
