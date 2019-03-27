## Tank node

Several `tanks` are supposed to be sparsely distributed in the `process area`. The proposed distributed architecture dedicates an exclusive node to monitor the water level, temperature, humidity, and luminance from each tank.

The `tank node` should be powered locally and communicate through a wireless link, then both electrical power and wireless signal should be available at tank area. It is also expected that the existing wireless LAN should be connected to the Internet.

The main specifications and features for the `tank node` are listed below.

### Raspberry Pi Zero W

Due to its low cost ARM11 core processor and built in wireless LAN, the `Pi Zero W` was selected to power the `tank node`. Its main features are:

- 1Ghz, Broadcom BCM 2835 single-core processor
- 512 MB of RAM
- 1 micro USB port for power supply
- Compatible with existing HATs
- Composite video and reset headers
- CSI Camera Connector
- 40-pin GPIO connector (same pinout as A+/B+/2B)
- On-board Wireless LAN – 2.4 GHz 802.11 b/g/n (BCM43438)
- On-board Bluetooth 4.1 + HS Low-energy (BLE) (BCM43438)

### Sensors

For this project, the following sensors were selected: 

- **Water level:** [VL53L1X](https://www.st.com/en/imaging-and-photonics-solutions/vl53l1x.html) - ToF (time of flight) sensor.
- **Temperature:** [HTU21D](https://www.mouser.com/pdfdocs/HTU21DF.PDF) - Digital Relative Humidity sensor with Temperature output.
- **Humidity:** [HTU21D](https://www.mouser.com/pdfdocs/HTU21DF.PDF) - Digital Relative Humidity sensor with Temperature output.
- **Luminance:** [BH1750](https://www.mouser.com/ds/2/348/bh1750fvi-e-186247.pdf)  - Digital 16bit Serial Output Type Ambient Light Sensor.

#### Water level
The water level sensor VL53L1X is installed inside the tank, as seen below, at the top. Then, the sensor measurement reflects the distance from the top of the tank to the water surface. This measurement allows calculating the water level and consequently the volume stored in the tank.

![](https://i.imgur.com/V5eEZaI.jpg)

The STMicroelectronics VL53L1X "time of flight sensor" is equipped with an invisible laser to measure distances with millimeter resolution. Please check the [full specs on the product page](https://www.st.com/en/imaging-and-photonics-solutions/vl53l1x.html) and the available [breakout](https://www.sparkfun.com/products/14722) shown below.

![](https://i.imgur.com/csxnBtA.jpg)

#### Temperature, humidity and luminance

Suppose a tank node equipped with a single set of these sensors. They may be installed in three positions:

- **Outside tank:** sensors outside the tank would measure environmental conditions in the tank area.
- **Inside tank, outside node:** these sensors would measure the internal tank conditions.
- **Inside tank, inside node:** these sensors would evaluate the internal conditions of the node itself.

The tank node prototype, shown upside down in the photo, has a VL53L1X sensor pointing down towards water direction. The Pi Zero W is tied to an [Anavi Infrared pHat](https://www.crowdsupply.com/anavi-technology/infrared-phat) with I2C connections for the three sensors.

![](https://i.imgur.com/MINoMZq.jpg)

The temperature, humidity and luminance sensors are installed inside the node, in order to evaluate internal prototype conditions. It is expected that internal temperature and humidity changes with CPU utilization, for example.

The luminance sensor actually measures light conditions inside the tank, since node prototype has a transparent case. Since VL53L1X performance may vary with light interference, an "open hatch" alarm may be created, in case light is detected inside the water tank. Also, open water tanks are a *very bad idea*, due to mosquito proliferation!





MQTT streaming generated at each tank node publishes the variables that should be monitored. A preliminary user interface is located at the tank supervisor, showing information from all tanks. This system may be easily scaled for many tanks and is smart enough to handle simple decisions.

The source code from an available Python 2 library should be upgraded to Python 3 in order to create a new "Time of Flight" platform for Home Assistant.




