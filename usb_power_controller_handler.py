from uhubctl import Hub,Port
def convert_state_str(state):
    if state:
        return "ON"
    return "OFF"


class UsbPowerControllerHandler:
    """USB Power Controller Object"""  # __doc__ / docstring

    VERSION = '0.1'

    # UHUBCTL object

    _usb_hub = None

    _usb_hub_str = None

    _current_state = True

    # State change callback
    # Signature on_state_change(state: bool)
    on_state_change = None

    # Logger callback
    on_log_message = None

    def __init__(self, _hub_str):
        self._usb_hub_str = _hub_str
        self._usb_hub = Hub(self._usb_hub_str, enumerate_ports=True)
        # Check if hub actually has anything in it
        if len(self._usb_hub.ports) is 0:
            raise ValueError("Invalid USB hub specified in configuration. Specified hub contains 0 ports")
            # TODO: Should ensure this error is caught in controller
        # Seems good, moving on...

    def set_state(self, state):
        self.log("Setting USB power state to: " + convert_state_str(state))
        # Raspberry pi: All port's power is disabled at the same time, so just take the first
        if self._usb_hub.ports[0].status == state:
            self.log("USB power state already " + convert_state_str(state))
            self._current_state = state
            return
        self.log("Changing USB power state to " + convert_state_str(state))
        self._current_state = state
        self._usb_hub.ports[0].status = state
        self.log("Current state as read from system is " + convert_state_str(self._usb_hub.ports[0].status))

        if self.on_state_change is not None:
            self.on_state_change(self.state_out())

    def state_out(self):
        return self._usb_hub.ports[0].status

    def log(self, message):
        if self.on_log_message is not None:
            self.on_log_message(message)

    def cleanup(self):
        self.log("Cleanup function unused")

