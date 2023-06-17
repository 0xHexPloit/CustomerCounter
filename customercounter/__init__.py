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


def _run_tui_program(events_rx: IEventReceiver):
    store = ElectronicDevicesStore.get_instance()
    event_manager = EventManager(store, events_rx)
    tui = CustomerCounterTUI(event_manager)
    tui.run()


def _run_sniffer_program(interface: str, events_tx: IEventTransmitter):
    settings = get_app_settings()
    event_pool = EventPool()
    event_collector = EventCollector(event_pool, events_tx, settings.collector.interval)
    event_collector.spawn()
    start_probe_requests_listener(interface, event_pool)


def run_program(interface: str):
    tx_rx_pipe = PipeEventTransmitterReceiver()

    process = multiprocessing.Process(
        target=_run_sniffer_program, args=(interface, tx_rx_pipe.get_transmitter())
    )
    process.start()

    _run_tui_program(tx_rx_pipe.get_receiver())
