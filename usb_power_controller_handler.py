import uhubctl


def convert_state_str(state):
    if state:
        return "ON"
    return "OFF"


class UsbPowerControllerHandler:
    """USB Power Controller Object"""  # __doc__ / docstring

    VERSION = '0.1'

    # UHUBCTL object
    _usb_power_ctl = None

    _usb_ports = list()

    _current_state = True

    # State change callback
    # Signature on_state_change(state: bool)
    on_state_change = None

    # Logger callback
    on_log_message = None

    def __init__(self):
        self._usb_power_ctl = uhubctl
        for hub in self._usb_power_ctl.discover_hubs():
            for port in hub:
                self._usb_ports.append(port)

    def set_state(self, state):
        self.log("Setting USB power state to: " + convert_state_str(state))
        # Raspberry pi: All ports power is disabled at the same time, so just take the first
        if self._usb_ports[0].status == state:
            self.log("USB power state already " + convert_state_str(state))
            self._current_state = state
            return
        self.log("Changing USB power state to " + convert_state_str(state))
        self._current_state = state
        self._usb_ports[0].status = state

        #for port in self._usb_ports:
        #    if port.status == state:
        #        self.log("USB power state already " + convert_state_str(state))
        #        self._current_state = state
        #        return
        #    self.log("Changing USB power state to " + convert_state_str(state))
        #    self._current_state = state
        #    port.status = state

    def get_state(self):
        return self._usb_ports[0].status

    def log(self, message):
        if self.on_log_message is not None:
            self.on_log_message(message)

    def cleanup(self):
        self.log("Cleanup function unused")

