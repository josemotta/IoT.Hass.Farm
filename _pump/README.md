## Pump node

At this time, only the supervision system is being considered. The process extracts water from a well that is 25 meters below surface and should move it to a water storage located 15 meters high, totaling 40 meters. In order to optimize energy and comply to equipment specs, the job is done in a couple steps. As listed below, a couple pumps work together to move the water from the well to the big water storage placed on the high tower:

- The first stage is twenty five meters below surface in the well, powered by a thin-vertical-pump, located inside the plumbs. It pushes water to a small intermediary tank at surface level.
- Another high-power-pump is responsible for moving the water from the intermediary tank to the big water storage placed on the high tower.
- The high-power-pump starts when the intermediary tank is full and stops when it is empty. The logic for this synchronization is already set and is not being considered here now. The focus is supervision and measurement of water flow.

The main specifications and features for the `pump node` are listed below.

### Raspberry Pi 3 Model B+

Due to its powerful ARMv8 processor and the amazing PoE capabilities, the `Pi 3 Model B+` was selected to power the `pump node`. The final revision in the Raspberry Pi 3 range has the following features:

- 1.4Ghz processor, Broadcom BCM2837B0, Cortex-A53 (ARMv8) 64-bit SoC
- 1GB LPDDR2 SDRAM
- 2.4GHz and 5GHz IEEE 802.11.b/g/n/ac wireless LAN, Bluetooth 4.2, BLE
- Gigabit Ethernet over USB 2.0 (maximum throughput 300 Mbps)
- Extended 40-pin GPIO header
- Full-size HDMI
- 4 USB 2.0 ports
- CSI camera port for connecting a Raspberry Pi camera
- DSI display port for connecting a Raspberry Pi touchscreen display
- 4-pole stereo output and composite video port
- Micro SD port for loading your operating system and storing data
- 5V/2.5A DC power input
- Power-over-Ethernet (PoE) support (requires separate PoE HAT)
- [Raspberry Pi PoE HAT](https://static.raspberrypi.org/files/product-briefs/Raspberry-Pi-PoE_HAT-Product-Brief.pdf) provides 5V DC/2.5A power from RJ-45 network port (PoE IEEE 802.3af)

### Sensors

For this project, the following sensors were selected:

- **ADC Analog Digital Converter:** Two options are being considered:
- [ADS1015 Ultra-Small, Low-Power, I2C-Compatible, 3.3-kSPS, 12-Bit ADCs With Internal Reference, Oscillator, and Programmable Comparator](http://www.ti.com/lit/ds/symlink/ads1015.pdf)
- [ADS1115 Ultra-Small, Low-Power, I2C-Compatible, 860-SPS, 16-Bit ADCs With Internal Reference, Oscillator, and Programmable Comparator](http://www.ti.com/lit/ds/symlink/ads1115.pdf)

- **Hall Current Detection Sensor:** Two options are being considered:
- [WCS1800 Hall Current Detection Sensor Module 35A Precise With Overcurrent Protection](https://www.banggood.com/search/dc-5v-wcs1800-hall-current-detection-sensor-module-35a-precise.html)
- [CJMCU-758 Linear Current Sensor Hall Current Module](https://www.banggood.com/search/3pcs-cjmcu-758-acs758lcb-050b-pff-t-linear-current-sensor.html)

- **Temperature:** [HTU21D](https://www.mouser.com/pdfdocs/HTU21DF.PDF) - Digital Relative Humidity sensor with Temperature output.
- **Humidity:** [HTU21D](https://www.mouser.com/pdfdocs/HTU21DF.PDF) - Digital Relative Humidity sensor with Temperature output.
- **Luminance:** [BH1750](https://www.mouser.com/ds/2/348/bh1750fvi-e-186247.pdf)  - Digital 16bit Serial Output Type Ambient Light Sensor.

#### ADC Analog Digital Converter

#### Hall Current Detection Sensor

#### Temperature, humidity and luminance

The pump node is equipped with a single set of these sensors. They may be installed in three positions:

- **Outside pump:** sensors outside would measure environmental conditions in the pump area.
- **Inside pump area, outside node:** these sensors would measure the conditions where pumps are installed.
- **Inside pump area, inside node:** these sensors would evaluate the internal conditions of the node itself.

The pump node prototype shown below is powered by a PoE HAT, located just above the Raspberry Pi 3B+. As you can notice, the prototype has just the network cable connected to provide both power and Ethernet communication. On the top of the HAT stack there is a [Qwiic pHAT](https://cdn.sparkfun.com/assets/9/c/4/8/6/Qwiic_pHat_for_Raspberry_Pi_v20.pdf) equipped with four connectors for I2C sensors. The photo also shows the HTU21D and BH1750 connected.

![Pump node](https://i.imgur.com/0aoOnIq.png)

The temperature, humidity and luminance sensors are installed inside the node, in order to evaluate internal prototype conditions. It is expected that internal temperature and humidity changes with CPU utilization, for example. The luminance sensor actually measures light conditions inside the pump area, since node prototype has a transparent case.

## Install Hass.io

The `Pi 3 Model B+` is supposed to be installed with following software:

- **Linux Raspbian GNU/Linux 9.1 (stretch)**. [Lite version](https://www.raspberrypi.org/downloads/raspbian/), the minimal image based on Debian Stretch. Generate the Micro SD Card with [Etcher](https://www.raspberrypi.org/magpi/pi-sd-etcher/), for example, and boot the RPI.
- If you need the configuration program **raspi-config**, it is already available at Stretch Lite version.
- You should also install **Git**, used to clone the IoT.Hass.farm repository.

```
$ sudo apt-get install git
```

Next step is installing Hass.io, easy with following script based on Dale Higgs [hassio-installer](https://github.com/josemotta/hassio-installer). Run the script below to install all requirements, including latest Docker version. Then, Hass.io is finally installed.

    curl -sL https://raw.githubusercontent.com/josemotta/hassio-installer/master/hassio_rpi3bp | bash -s

You should have now the latest version of Homeassistant running. You can start the frontend, using a browser, and enter the IP address of prototype followed by port 8123. For example:

```
http://192.168.0.112:8123
```
## Clone the repo

The next step will replace the Homeassistant config directory with IoT.Hass.Farm (or your customized fork).

- Stop Homeassistant, using Hass.io developer tools, click `Services` and select `homeassistant.stop`;
- Clear the Homeassistant configuration located at `/usr/share/hassio/homeassistant`;
- Clone the IoT.Hass.Farm repository inside this folder;
- Run `./set-config.sh pump` script to initialize configuration folder;
- Set your secrets file;
- And finally reboot.

After you stop Homeassistant, replacement is done with the following commands, as shown below:

```
$ cd /usr/share/hassio/homeassistant
$ sudo rm -rf ./*
$ sudo rm -rf ./.*

$ sudo git clone https://github.com/josemotta/IoT.Hass.Farm.git .
Cloning into '.'...
remote: Enumerating objects: 201, done.
remote: Counting objects: 100% (201/201), done.
remote: Compressing objects: 100% (137/137), done.
remote: Total 201 (delta 123), reused 134 (delta 60), pack-reused 0
Receiving objects: 100% (201/201), 43.18 KiB | 0 bytes/s, done.
Resolving deltas: 100% (123/123), done.

$ sudo ./set-config.sh pump

$ ls -l
-rw-r--r-- 1 root root        2 Jul 31 21:48 automations.yaml
-rwxr--r-- 1 root root     4123 Jul 31 22:22 configuration.yaml
-rw-r--r-- 1 root root      742 Jul 31 21:48 customize.yaml
drwxr-xr-x 2 root root     4096 Jul 31 21:58 deps
-rw-r--r-- 1 root root        0 Jul 31 21:48 groups.yaml
-rw-r--r-- 1 root root    35149 Jul 31 21:48 LICENSE
drwxr-xr-x 3 root root     4096 Jul 31 22:09 _pump
-rw-r--r-- 1 root root     7946 Jul 31 21:48 README.md
-rw-r--r-- 1 root root        0 Jul 31 21:48 scripts.yaml
-rwxr--r-- 1 root root     1171 Jul 31 23:04 secrets-dummy.yaml
-rwxr-xr-x 1 root root      606 Jul 31 21:48 set-config.sh
drwxr-xr-x 3 root root     4096 Jul 31 21:48 _super
drwxr-xr-x 3 root root     4096 Jul 31 21:48 _tank
-rw-r--r-- 1 root root     4253 Jul 31 21:48 themes.yaml
-rwxr--r-- 1 root root     1241 Jul 31 22:23 ui-lovelace.yaml
-rw-r--r-- 1 root root     1389 Jul 31 21:48 zones.yaml

$ sudo mv secrets-dummy.yaml secrets.yaml
$ sudo reboot
```

After the boot you can check packages being dynamically loaded. Open the browser and enter the IP address of prototype followed by port 8123 to start the user interface. In the first use an user id and password will be required to create the admin account.

![](https://i.imgur.com/3pLBjM2.jpg)

The MQTT streaming generated at each tank node publishes all sensor data that should be monitored.  This system may be easily scaled for many tanks and is smart enough to handle simple decisions.

