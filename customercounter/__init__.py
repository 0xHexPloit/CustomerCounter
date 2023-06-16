import multiprocessing

from customercounter.electronic_device.store import ElectronicDevicesStore
from customercounter.event.collector import EventCollector
from customercounter.event.manager import EventManager
from customercounter.event.pool import EventPool
from customercounter.event.receiver import IEventReceiver
from customercounter.event.transmitter import IEventTransmitter
from customercounter.event.transmitter_receiver import PipeEventTransmitterReceiver
from customercounter.network.sniffer import start_probe_requests_listener
from customercounter.settings import get_app_settings
from customercounter.tui import CustomerCounterTUI


def run_tui_program(rx_event: IEventReceiver):
    devices_store = ElectronicDevicesStore.get_instance()
    event_manager = EventManager(devices_store, rx_event)
    tui = CustomerCounterTUI(event_manager)
    tui.run()


def run_sniffer_program(interface: str, tx_event: IEventTransmitter):
    config = get_app_settings()
    event_pool = EventPool()
    event_collector = EventCollector(event_pool, tx_event, config.collector.interval)
    event_collector.spawn()

    start_probe_requests_listener(interface, event_pool)


def run_program(interface: str):
    tx_rx_pipe = PipeEventTransmitterReceiver()

    # Running sniffer program
    process = multiprocessing.Process(
        target=run_sniffer_program, args=(interface, tx_rx_pipe.get_transmitter())
    )
    process.start()

    # Running tui program
    run_tui_program(tx_rx_pipe.get_receiver())
