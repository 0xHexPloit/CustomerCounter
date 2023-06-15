from multiprocessing import Pipe

from customercounter.event.event import Event
from customercounter.event.transmitter import PipeEventTransmitter


def test_should_send_events_in_the_pipe(event):
    rx, tx = Pipe(duplex=False)
    event_transmitter = PipeEventTransmitter(tx)
    event_transmitter.send([event])
    received_events: list[Event] = rx.recv()

    assert len(received_events) == 1
    assert received_events[0].device_id == event.device_id
    assert received_events[0].os == event.os
