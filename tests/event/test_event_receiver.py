from multiprocessing import Pipe

from customercounter.event.event import Event
from customercounter.event.receiver import PipeEventReceiver


def test_should_get_events_from_pipe(event: Event):
    rx, tx = Pipe(duplex=False)
    event_receiver = PipeEventReceiver(rx=rx)
    tx.send([event])
    received_events = event_receiver.get_events()

    assert len(received_events) == 1
    assert received_events[0].device_id == event.device_id
    assert received_events[0].os == event.os
