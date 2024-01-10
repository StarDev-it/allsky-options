from gpiozero import DigitalOutputDevice


# Relay pins in BCM mode
pin_relay0 = 4
pin_relay1 = 22
pin_relay2 = 6
pin_relay3 = 26


class RelayFactory:
    """
    This is the relay factory
    Add/Modify the config to assign the right device type
    """
    config = {
        'DewHeater': pin_relay0,
        'Fan': pin_relay1
    }

    @staticmethod
    def create(device_type=None):
        """
        Create a new Relay instance
        :param device_type: string
        :return:
        """
        if device_type is None or device_type not in RelayFactory.config:
            raise ValueError('The device type %s not exists' % device_type)
        return Relay(RelayFactory.config[device_type])


class Relay:
    """
    Common relay class
    """
    relay = None

    def __init__(self, relay_pin):
        """
        Manage relay output port
        Initialize relay pins in BCM mode
        :param relay_pin: int
        """
        self.relay = DigitalOutputDevice(relay_pin)

    def enable(self):
        """
        Enable relay
        """
        self.relay.on()

    def disable(self):
        """
        Disable relay
        """
        self.relay.off()

    @property
    def is_enabled(self):
        """
        Check if relay is enabled
        """
        return bool(self.relay.value)
