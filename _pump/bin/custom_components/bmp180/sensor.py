"""BMP180 - Temperature & Atmospheric Pressure Sensor."""

import asyncio
import logging
from functools import partial

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.components import rpi_gpio
from homeassistant.const import CONF_NAME, TEMP_FAHRENHEIT, TEMP_CELSIUS, PRESSURE_HPA
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

LENGTH_MILLIMETERS = "mm"

CONF_I2C_ADDRESS = "i2c_address"
CONF_I2C_BUS = "i2c_bus"

DEFAULT_NAME = "BMP180"
DEFAULT_I2C_ADDRESS = 0x77
DEFAULT_I2C_BUS = 1

SENSOR_TEMPERATURE = "temperature"
SENSOR_PRESSURE = "pressure"

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
    """Reset and initialize the VL53L1X ToF Sensor from STMicroelectronics."""
    #import smbus  # pylint: disable=import-error
    from sensor.BMP180 import BMP180  # pylint: disable=import-error

    name = config.get(CONF_NAME)
    bus_number = config.get(CONF_I2C_BUS)
    i2c_address = config.get(CONF_I2C_ADDRESS)
    temp_unit = hass.config.units.temperature_unit

    sensor = await hass.async_add_executor_job(partial(BMP180, bus_number, i2c_address))
    # await hass.async_add_executor_job(init_bmp, bus_number, i2c_address, sensor)
    # await asyncio.sleep(0.01)

    dev = [
        BMP180Sensor(sensor, name, SENSOR_TEMPERATURE, temp_unit),
        BMP180Sensor(sensor, name, SENSOR_PRESSURE, PRESSURE_HPA),
    ]

    async_add_entities(dev, True)


class BMP180Sensor(Entity):
    """Implementation of BMP180 sensor."""

    def __init__(self, bmp180_sensor, name, variable, unit):
        """Initialize the sensor."""
        self.bmp180_sensor = bmp180_sensor
        self._name = "{}_{}".format(name, variable)
        self._variable = variable
        self._unit_of_measurement = unit
        self._state = None

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
        if self._variable == SENSOR_TEMPERATURE:
            if self.unit_of_measurement == TEMP_CELSIUS:
                value = self.bmp180_sensor.temperature().C
            if self.unit_of_measurement == TEMP_FAHRENHEIT:
                value = self.bmp180_sensor.temperature().F
        else:
            value = self.bmp180_sensor.pressure().hPa
        self._state = value
