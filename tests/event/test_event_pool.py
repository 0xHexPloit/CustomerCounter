from customercounter.event.pool import EventPool


def test_pool_should_be_empty():
    pool = EventPool()
    pool_size = pool.get_pool_size()

    assert pool_size == 0


def test_should_be_possible_to_add_event_in_the_pool(event):
    pool = EventPool()
    pool.add_event(event)
    pool_size = pool.get_pool_size()

    assert pool_size == 1


def test_should_be_possible_to_get_all_the_items_in_the_pool_and_clear_content(event):
    pool = EventPool()
    pool.add_event(event)
    events = pool.remove_all_events()

    assert len(events) == 1
    assert events[0] is event


def test_pool_should_not_store_duplicates(event):
    pool = EventPool()
    pool.add_event(event)
    pool.add_event(event)
    pool_size = pool.get_pool_size()

    assert pool_size == 1
