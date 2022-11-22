import configparser

from random import choice

class UsbPowerControllerConfigurationHandler:
    DEVICE_NAME = None  # type: str
    MQTT_HOST = None  # type: str
    MQTT_PORT = None  # type: int
    MQTT_CLIENT_ID = None  # type: str
    MQTT_USE_AUTHENTICATION = None  # type: bool
    MQTT_USERNAME = None  # type: str
    MQTT_PASSWORD = None  # type: str
    MQTT_USE_SSL = None  # type: bool
    MQTT_PORT_SSL = None  # type: int
    MQTT_TOPIC_SET_USB_POWER_STATE = None  # type: str
    MQTT_TOPIC_REPORT_USB_POWER_STATE = None  # type: str

    _hexdigits = '0123456789abcdef'

    def generate_client_id(self):
        self.MQTT_CLIENT_ID = 'usb_power_controller_' + ''.join(choice(self._hexdigits) for _ in range(32))

    # Config parsing helpers
    @staticmethod
    def bool_parse(str_value: str, var_name: str, default: bool) -> object:
        val = str.lower(str_value)
        if val == '':
            return default
        if val == 'true' or val == 'high' or val == '1':
            return True
        if val == 'false' or val == 'low' or val == '0':
            return False
        raise TypeError('Config value "' + str_value + '" is invalid for ' + var_name)

    @staticmethod
    def int_parse(str_value: str, var_name: str, can_be_none: bool) -> object:
        if (str_value == '' or str_value is None) and can_be_none:
            return None
        if (str_value == '' or str_value is None) and not can_be_none:
            raise ValueError("Config value cannot be empty for " + var_name)
        return int(str_value)

    @staticmethod
    def float_parse(str_value: str, var_name: str, can_be_none: bool) -> object:
        if (str_value == '' or str_value is None) and can_be_none:
            return None
        if (str_value == '' or str_value is None) and not can_be_none:
            raise ValueError("Config value cannot be empty for " + var_name)
        return float(str_value)

    @staticmethod
    def str_parse(str_value: str, var_name: str, can_be_none: bool) -> object:
        if str_value == '' and can_be_none:
            return None
        if str_value == '' and not can_be_none:
            raise TypeError('Config value is invalid for ' + var_name + ': value cannot be empty')
        return str(str_value)

    def get_port(self):
        if self.MQTT_USE_SSL:
            return self.MQTT_PORT_SSL
        return self.MQTT_PORT

    def __init__(self, config_file):

        config = configparser.ConfigParser()
        config.read(config_file)

        self.USB_POWER_NAME = self.\
            str_parse(config['General']['switch_name'],
                      'switch_name',
                      False)
        self.MQTT_HOST = self.\
            str_parse(config['MQTTBrokerConfig']['mqtt_host'],
                      'mqtt_host',
                      False)
        self.MQTT_PORT = self.\
            int_parse(config['MQTTBrokerConfig']['mqtt_port'],
                      'mqtt_port',
                      False)
        self.MQTT_CLIENT_ID = self.\
            str_parse(config['MQTTBrokerConfig']['mqtt_client_id'],
                      'mqtt_client_id',
                      True)
        self.MQTT_USE_AUTHENTICATION = self.\
            bool_parse(config['MQTTBrokerConfig']['mqtt_use_authentication'],
                       'mqtt_use_authentication',
                       False)
        self.MQTT_USERNAME = self.\
            str_parse(config['MQTTBrokerConfig']['mqtt_username'],
                      'mqtt_username',
                      not self.MQTT_USE_AUTHENTICATION)
        self.MQTT_PASSWORD = self.\
            str_parse(config['MQTTBrokerConfig']['mqtt_password'],
                      'mqtt_password',
                      not self.MQTT_USE_AUTHENTICATION)
        self.MQTT_USE_SSL = self.\
            bool_parse(config['MQTTBrokerConfig']['mqtt_use_ssl'],
                       'mqtt_use_ssl',
                       False)
        self.MQTT_PORT_SSL = self.\
            int_parse(config['MQTTBrokerConfig']['mqtt_port_ssl'],
                      'mqtt_port_ssl',
                      not self.MQTT_USE_SSL)
        self.MQTT_TOPIC_SET_USB_POWER_STATE = self.\
            str_parse(config['MQTTTopicConfig']['mqtt_topic_set_switch_state'],
                      'mqtt_topic_set_switch_state',
                      False)
        self.MQTT_TOPIC_REPORT_USB_POWER_STATE = self.\
            str_parse(config['MQTTTopicConfig']['mqtt_topic_report_switch_state'],
                      'mqtt_topic_report_switch_state',
                      False)

        if self.MQTT_CLIENT_ID == '' or self.MQTT_CLIENT_ID is None:
            self.generate_client_id()
