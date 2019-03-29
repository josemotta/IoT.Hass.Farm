## Tank node

Several `tanks` are supposed to be sparsely distributed in the `process area`. The proposed distributed architecture dedicates an exclusive node to monitor the water level, temperature, humidity, and luminance from each tank.

The `tank node` should be powered locally and communicate through a wireless link, then both electrical power and wireless signal should be available at tank area. It is also expected that the existing wireless LAN should be connected to the Internet.

The main specifications and features for the `tank node` are listed below.

### Raspberry Pi Zero W

Due to low cost option with powerful ARM11 core processor and built in wireless LAN, the `Pi Zero W` was selected to power the `tank node`. Its main features are:

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

The tank node prototype, shown upside down in the photo, has a VL53L1X sensor pointing down towards water direction. The Pi Zero W is tied to an [Anavi Infrared pHat](https://www.crowdsupply.com/anavi-technology/infrared-phat) with I2C connections for the three sensors. The temperature, humidity and luminance sensors are installed inside the node, in order to evaluate internal prototype conditions. It is expected that internal temperature and humidity changes with CPU utilization, for example.

![](https://i.imgur.com/MINoMZq.jpg)

The luminance sensor actually measures light conditions inside the tank, since node prototype has a transparent case. Since VL53L1X performance may vary with light interference, an "open hatch" alarm may be created, in case light is detected inside the water tank. Also, open water tanks are a *very bad idea*, due to mosquito proliferation!

## Install Hass.io

The `Pi Zero W` is supposed to be installed with following software:

- **Linux Raspbian GNU/Linux 9.1 (stretch)**. [Lite version](https://www.raspberrypi.org/downloads/raspbian/), the minimal image based on Debian Stretch. Generate the Micro SD Card with [Etcher](https://www.raspberrypi.org/magpi/pi-sd-etcher/), for example, and boot the RPI.
- If you need the configuration program raspi-config, it is already available at Stretch Lite version.

Next step is installing Hass.io, easier task with Dale Higgs [hassio-installer](https://github.com/josemotta/hassio-installer). Run the script below to install all requirements, including the latest Docker version that works fine with `Pi Zero W`. Then, Hass.io is also installed.

    curl -sL https://github.com/josemotta/hassio-installer/blob/master/hassio_rpi0w | bash -s

You should have now the latest version of Homeassistant running at the prototype.

## Install Git

## Clone the repo

- Stop Homeassistant, using Hass.io developer tools, click `Services` and select `homeassistant.stop`;
- Clear the Homeassistant configuration located at `/usr/share/hassio/homeassistant`;
- Clone the IoT.Hass.Farm repository inside the folder;
- Run `./set-config.sh tank` script to initialize configuration folder;
- Restart Homeassistant, use Hass.io developer tools again, this time select `homeassistant.restart`.

```
$ cd /usr/share/hassio/homeassistant
$ sudo rm -rf ./*
$ sudo rm -rf ./.*
$ sudo git clone git@github.com:josemotta/IoT.Hass.Farm.git .
Cloning into '.'...
remote: Enumerating objects: 201, done.
remote: Counting objects: 100% (201/201), done.
remote: Compressing objects: 100% (137/137), done.
remote: Total 201 (delta 123), reused 134 (delta 60), pack-reused 0
Receiving objects: 100% (201/201), 43.18 KiB | 0 bytes/s, done.
Resolving deltas: 100% (123/123), done.
$ sudo ./set-config.sh tank
$ ls -l
total 88
-rw-r--r-- 1 root root     2 Mar 29 20:38 automations.yaml
-rw-r--r-- 1 root root  4050 Mar 29 20:38 configuration.yaml
-rw-r--r-- 1 root root   742 Mar 29 20:36 customize.yaml
-rw-r--r-- 1 root root     0 Mar 29 20:36 groups.yaml
-rw-r--r-- 1 root root 35149 Mar 29 20:36 LICENSE
-rw-r--r-- 1 root root  5283 Mar 29 20:38 README.md
-rw-r--r-- 1 root root     0 Mar 29 20:36 scripts.yaml
-rw-r--r-- 1 root root   818 Mar 29 20:36 secrets-dummy.yaml
-rwxr-xr-x 1 root root   284 Mar 29 20:36 set-config.sh
drwxr-xr-x 2 root root  4096 Mar 29 20:36 _super
drwxr-xr-x 2 root root  4096 Mar 29 20:36 _tank
-rw-r--r-- 1 root root  4253 Mar 29 20:38 themes.yaml
-rw-r--r-- 1 root root  1051 Mar 29 20:38 ui-lovelace.yaml
-rw-r--r-- 1 root root  1389 Mar 29 20:36 zones.yaml
$ sudo mv secrets-dummy.yaml secrets.yaml
$ sudo reboot
```

After the boot you can check that packages are being dynamically loaded at `config/deps` folder, as shown below. You may have to reboot a second time to start using VL53L1X, but it runs smoothly after that.

![](https://i.imgur.com/Bg4gx0R.jpg)

In the first use an user id and password will be required to create the admin account.

MQTT streaming generated at each tank node publishes the variables that should be monitored. A preliminary user interface is located at the tank supervisor, showing information from all tanks. This system may be easily scaled for many tanks and is smart enough to handle simple decisions.

The source code from an available Python 2 library should be upgraded to Python 3 in order to create a new "Time of Flight" platform for Home Assistant.
