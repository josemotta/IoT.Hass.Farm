from homeassistant.helpers.entity import Entity
import time
# Import the ADS1x15 module.
import Adafruit_ADS1x15

GAIN = 1
ADC_INPUT = 0

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    add_devices([ads_o2()])


class ads1X15(Entity):
    """Representation of a Sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._state = None
        # Create an ADS1115 ADC (16-bit) instance.
        self._adc = Adafruit_ADS1x15.ADS1115()

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'O2 Level'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "%"

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._adc.read_adc(ADC_INPUT, gain=GAIN)