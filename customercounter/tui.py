import multiprocessing

import numpy as np
import textual.widgets as widgets
from textual.app import App, ComposeResult

from customercounter.electronic_device.state_machine import (
    ElectronicDevicePresenceMachineState,
)
from customercounter.electronic_device.store import ElectronicDevicesStore
from customercounter.event.manager import IEventManager
from customercounter.operating_system import OperatingSystem

CURRENT_SHOPPERS_MESSAGE = """
Current number of shoppers in the mall: {}
"""

OS_DEVICE_MESSAGE = """
Distribution of devices per operating system: \n
    - Apple: {:.2f} %
    - Android: {:.2f} %
    - Other: {:.2f} %
"""

TOTAL_SHOPPERS_MESSAGE = """
Total number of shoppers since launch: {}
"""

SPENT_TIME_MESSAGE = """
Average time spent by shopper in the mall since launch: {}
"""


class CustomerCounterTUI(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("e", "exit", "Exit")]

    def __init__(self, event_manager: IEventManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__manager = event_manager
        self.__manager.add_subscriber(self)

    def compose(self) -> ComposeResult:
        header = widgets.Header(name="CustomerCounter", show_clock=True)
        header.tall = True

        yield header
        yield widgets.Label(CURRENT_SHOPPERS_MESSAGE.format(0), id="current_shoppers")
        yield widgets.Label(OS_DEVICE_MESSAGE.format(0, 0, 0), id="operating_system")
        yield widgets.Label(TOTAL_SHOPPERS_MESSAGE.format(0), id="total_shoppers")
        yield widgets.Label(SPENT_TIME_MESSAGE.format("nan"), id="time_spent")
        yield widgets.Footer()

        self.__manager.spawn()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_exit(self) -> None:
        """An action to quit the program"""

        # Getting active children
        active_children = multiprocessing.active_children()
        for child in active_children:
            child.kill()
        exit(0)

    def handle_store_update(self):
        store = ElectronicDevicesStore.get_instance()

        current_number_shoppers = 0

        apple_devices = 0
        android_devices = 0
        other_devices = 0

        total_number_shoppers = 0

        average_time = []

        devices = store.get_electronic_devices()

        for device in devices:
            # Checking if the shopper is in the mall
            device_state = device.get_current_state()

            if (
                device_state == ElectronicDevicePresenceMachineState.IN_MALL
                or device_state
                == ElectronicDevicePresenceMachineState.POTENTIAL_LEAVING
            ):
                current_number_shoppers += 1

                # Checking the operating system of the device
                operating_system = device.get_os()

                if operating_system == OperatingSystem.APPLE:
                    apple_devices += 1
                elif operating_system == OperatingSystem.ANDROID:
                    android_devices += 1
                else:
                    other_devices += 1

            # Updating total number shoppers
            total_number_shoppers += len(device.get_in_mall_timestamps())

            # Computing average time
            arrival_timestamps = device.get_in_mall_timestamps()
            departure_timestamps = device.get_left_timestamps()

            for idx in range(len(departure_timestamps)):
                arrival_timestamps = arrival_timestamps[idx]
                departure_timestamp = departure_timestamps[idx]

                delta = departure_timestamp - arrival_timestamps

                average_time.append(delta)

        # Updating the labels
        if len(devices) == 0:
            return

        current_shoppers_label = self.query_one("#current_shoppers", widgets.Label)
        os_label = self.query_one("#operating_system", widgets.Label)
        total_shoppers_label = self.query_one("#total_shoppers", widgets.Label)
        average_time_label = self.query_one("#time_spent", widgets.Label)

        current_shoppers_label.update(
            CURRENT_SHOPPERS_MESSAGE.format(current_number_shoppers)
        )

        if current_number_shoppers != 0:
            os_label.update(
                OS_DEVICE_MESSAGE.format(
                    round(apple_devices / current_number_shoppers, 2) * 100,
                    round(android_devices / current_number_shoppers, 2) * 100,
                    round(other_devices / current_number_shoppers, 2) * 100,
                )
            )

        total_shoppers_label.update(
            TOTAL_SHOPPERS_MESSAGE.format(total_number_shoppers)
        )

        average_time_label.update(SPENT_TIME_MESSAGE.format(np.mean(average_time)))
