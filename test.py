from customercounter.electronic_device.electronic_device import ElectronicDevice
from customercounter.event.type import EventType

device = ElectronicDevice(device_id="AE-ED-32", vendor="Apple")
device.update_device_state(EventType.PROBE_REQUEST_RECEIVED)
device.update_device_state(EventType.NO_PROBE_REQUEST_RECEIVED)

