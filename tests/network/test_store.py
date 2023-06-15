from customercounter.network.store import MacAddressStore

DEFAULT_MAC_ADDRESS = "00-B0-D0-63-C2-26"


def test_store_should_be_empty_when_instantiated():
    store = MacAddressStore()
    mac_addresses = store.get_mac_addresses()
    assert len(mac_addresses) == 0


def test_store_should_add_new_item():
    store = MacAddressStore()
    store.add(DEFAULT_MAC_ADDRESS)
    mac_addresses = store.get_mac_addresses()
    assert len(mac_addresses) == 1


def test_store_should_not_contain_duplicate():
    store = MacAddressStore()
    store.add(DEFAULT_MAC_ADDRESS)
    store.add(DEFAULT_MAC_ADDRESS)
    mac_addresses = store.get_mac_addresses()
    assert len(mac_addresses) == 1


def test_should_return_that_an_item_is_present_in_the_store_if_it_is_true():
    store = MacAddressStore()
    store.add(DEFAULT_MAC_ADDRESS)
    assert store.does_contain(DEFAULT_MAC_ADDRESS)


def test_should_return_that_an_item_is_not_present_if_it_is_not_in_the_store():
    store = MacAddressStore()
    assert not store.does_contain(DEFAULT_MAC_ADDRESS)
