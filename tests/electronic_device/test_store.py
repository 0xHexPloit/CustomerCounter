from customercounter.electronic_device.electronic_device import ElectronicDevice
from customercounter.electronic_device.store import ElectronicDevicesStore


def test_should_get_an_empty_list_of_electronic_devices():
    store = ElectronicDevicesStore.get_instance()
    electronic_devices = store.get_electronic_devices()

    assert len(electronic_devices) == 0


def test_should_be_able_to_add_electronic_device_in_storage():
    device = ElectronicDevice("", "")
    store = ElectronicDevicesStore.get_instance()
    store.add_electronic_device(device)
    electronic_devices = store.get_electronic_devices()

    assert len(electronic_devices) == 1


def test_should_be_able_to_retrieve_a_device():
    device = ElectronicDevice("", "")
    store = ElectronicDevicesStore.get_instance()
    store.add_electronic_device(device)
    retrieved_device = store.get_electronic_device(device.get_id())

    assert retrieved_device.get_id() == device.get_id()


def test_should_return_none_if_device_not_in_storage():
    store = ElectronicDevicesStore.get_instance()
    retrieved_device = store.get_electronic_device("AAA")

    assert retrieved_device is None


def test_should_be_able_to_clear_storage():
    device = ElectronicDevice("", "")
    store = ElectronicDevicesStore.get_instance()
    store.add_electronic_device(device)
    store.clear_storage()
    electronic_devices = store.get_electronic_devices()

    assert len(electronic_devices) == 0
