from loguru import logger
from scapy.all import Packet, sniff
from scapy.layers.dot11 import Dot11ProbeReq


def handle_probe_request_packet(packet: Packet):
    if not packet.haslayer(Dot11ProbeReq):
        return
    logger.info(packet)


def start_probe_requests_listener(interface: str):
    logger.info(f"Starting listening for probe requests on interface: {interface} !")
    sniff(iface=interface, prn=handle_probe_request_packet)
