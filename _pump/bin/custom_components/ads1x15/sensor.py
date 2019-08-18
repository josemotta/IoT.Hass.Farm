"""ADS1x15 - Analog to Digital Converter."""

import asyncio
import logging
from functools import partial

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.components import rpi_gpio
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

POWER_VOLT = "V"

SENSOR_CH0 = "0"
SENSOR_CH1 = "1"

CONF_I2C_ADDRESS = "i2c_address"
CONF_I2C_BUS = "i2c_bus"

DEFAULT_NAME = "ADS1X15"
DEFAULT_I2C_ADDRESS = 0x48
DEFAULT_I2C_BUS = 1
DEFAULT_GAIN = 1

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_I2C_ADDRESS, default=DEFAULT_I2C_ADDRESS): vol.Coerce(int),
        vol.Optional(CONF_I2C_BUS, default=DEFAULT_I2C_BUS): vol.Coerce(int),
    }
)


# def init_bmp(bus_number, i2c_address, sensor):
#     """XSHUT port LOW resets the device."""
#     sensor(bus_number, i2c_address)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Reset and initialize the ADS1x15 Analog to Digital Converter."""

    import smbus  # pylint: disable=import-error
    import board  # pylint: disable=import-error
    import busio  # pylint: disable=import-error
    import adafruit_ads1x15.ads1015 as ADS  # pylint: disable=import-error
    from adafruit_ads1x15.analog_in import AnalogIn  # pylint: disable=import-error

    name = config.get(CONF_NAME)
    # bus_number = config.get(CONF_I2C_BUS)
    # i2c_address = config.get(CONF_I2C_ADDRESS)

    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)

    sensor = await hass.async_add_executor_job(partial(ADS.ADS1015, i2c))
    
    # sensor = await hass.async_add_executor_job(partial(ADS.ADS1015, i2c_address, bus_number))
    # await hass.async_add_executor_job(init_bmp, bus_number, i2c_address, sensor)
    # await asyncio.sleep(0.01)

    dev = [
        ADS1X15Sensor(sensor, name, SENSOR_CH0, AnalogIn),
        ADS1X15Sensor(sensor, name, SENSOR_CH1, AnalogIn),
    ]

    async_add_entities(dev, True)


class ADS1X15Sensor(Entity):
    """Implementation of ADS1X15 sensor."""

    def __init__(self, ads1x15_sensor, name, channel, analogin):
        """Initialize the sensor."""
        self._sensor = ads1x15_sensor
        self._name = "{}_{}".format(name, channel)
        self._unit_of_measurement = POWER_VOLT
        self._state = None
        self._chan = None
        self._channel = channel
        self._analogin = analogin
        # if channel == SENSOR_CH0:
        #     self._channel = None
        # if channel == SENSOR_CH1:
        #     self._channel = 1
        self.init = True

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return self._unit_of_measurement

    def update(self):
        """Get the latest measurement and update state."""
        if self.init:
            self.init = False
            if self._channel == SENSOR_CH0:
                self._chan = self._analogin(self._sensor, self._sensor.P0, self._sensor.P1)
            if self._channel == SENSOR_CH1:
                self._chan = self._analogin(self._sensor, self._sensor.P2, self._sensor.P3)

        #value = self.ads1x15_sensor.read_adc_difference(self._channel, DEFAULT_GAIN)
        self._state = self._chan.voltage
