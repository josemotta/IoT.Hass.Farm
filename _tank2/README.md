## Tank node 2

At this project, some improvements were considered after the first [_tank](https://github.com/josemotta/IoT.Hass.Farm/tree/master/_tank) version, opening new use cases for the `IoT.Hass.Farm` architecture. Please check [_tank](https://github.com/josemotta/IoT.Hass.Farm/tree/master/_tank) before reading this. 

The first version used a Raspberry Pi Zero W, the lowest cost option that performed very well to get precise distance measurements and redirect them to the supervisor node. Thanks to the MQTT protocol, the distance, temperature, humidity and luminance measurements form a data stream constantly moving from tiny RPi-Zero-W. This  solution supposes that the data stream will be properly analyzed  at `_super` node, in order to make further decisions about the process behavior.

The RPi-Zero-W limits the LAN connection to Wifi. This is a low cost option if you already have the Wifi signal on the air, otherwise it is necessary to purchase an reliable Access Point (AP). This is also a weak point because AP failure definitely affects data stream arrival to upper node levels, responsible for further process decisions.

The new tank sensor version 2:

- Does not depend on the Wifi, connecting to the LAN directly by a TP cable with RJ-45 connector;
- Has enough CPU power to analyze and apply smart algorithms for the time series data.

The main specifications and features for the `_tank2` node are listed below.

### Raspberry Pi 3 Model B+

Due to its powerful ARMv8 processor, the `Raspberry Pi 3 Model B+` was selected to power the `_tank2` node. It has the following features:

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

Same original sensors were selected:

- **Water level:** [VL53L1X](https://www.st.com/en/imaging-and-photonics-solutions/vl53l1x.html) - ToF (time of flight) sensor.
- **Temperature:** [HTU21D](https://www.mouser.com/pdfdocs/HTU21DF.PDF) - Digital Relative Humidity sensor with Temperature output.
- **Humidity:** [HTU21D](https://www.mouser.com/pdfdocs/HTU21DF.PDF) - Digital Relative Humidity sensor with Temperature output.
- **Luminance:** [BH1750](https://www.mouser.com/ds/2/348/bh1750fvi-e-186247.pdf)  - Digital 16bit Serial Output Type Ambient Light Sensor.

Please check [_tank](https://github.com/josemotta/IoT.Hass.Farm/tree/master/_tank) for more details.

## Install Hass.io

The `RPi-3B+` is supposed to be installed with following software:

- **Linux Raspbian GNU/Linux 9.1 (stretch)**. [Lite version](https://www.raspberrypi.org/downloads/raspbian/), the minimal image based on Debian Stretch. Generate the Micro SD Card with [Etcher](https://www.raspberrypi.org/magpi/pi-sd-etcher/), for example, and boot the RPI.
- If you need the configuration program **raspi-config**, it is already available at Stretch Lite version.
- You should also install **Git**, used to clone the IoT.Hass.farm repository.

```
$ sudo apt-get install git
```

Next step is installing Hass.io, easy with following script based on Dale Higgs [hassio-installer](https://github.com/josemotta/hassio-installer). Run the script below to install all requirements, including latest Docker version. Then, Hass.io is finally installed.

    curl -sL https://raw.githubusercontent.com/josemotta/hassio-installer/master/hassio_rpi3bp | bash -s

You should have now the latest version of Homeassistant running. You can start the frontend, using a browser, and enter the IP address of prototype followed by port 8123.

## Set IP address

In order to change the `_tank2` node from automatic IP to a fixed IP, for example `192.168.0.233`, use the Network Manager Client, or `nmcli`. It is already installed, you just need to type the following commands to change the existing connection:

	pi@pump:~ $ nmcli con sh -a
	NAME                UUID                                  TYPE            DEVICE
	Wired connection 1  09cd6302-8894-3c8d-a84b-535ad6f38a73  802-3-ethernet  eth0
	docker0             e9d7ff39-304b-4a90-9498-dfcac41661ea  bridge          docker0
	hassio              d4ababb5-3cd8-4faa-b0cf-2ff72251e7a3  bridge          hassio

	pi@pump:~ $ sudo nmcli con edit "Wired connection 1"
	
	===| nmcli interactive connection editor |===
	
	Editing existing '802-3-ethernet' connection: 'Wired connection 1'
	
	Type 'help' or '?' for available commands.
	Type 'describe [<setting>.<prop>]' for detailed property description.
	
	You may edit the following settings: connection, 802-3-ethernet (ethernet), 802-1x, dcb, ipv4, ipv6, proxy
	nmcli> set ipv4.method manual
	nmcli> set ipv4.addresses 192.168.0.233/24
	nmcli> set ipv4.gateway 192.168.0.1
	nmcli> set ipv4.dns 192.168.0.1
	nmcli> save
	Connection 'Wired connection 1' (09cd6302-8894-3c8d-a84b-535ad6f38a73) successfully updated.
	nmcli> q

The `Wired connection 1` is now configured at `192.168.0.233`. To test, use a browser to start the frontend, entering the IP address followed by port 8123. In this case:

```
http://192.168.0.233:8123
```

## Clone the repo

The next step will replace the Homeassistant config directory with IoT.Hass.Farm (or your customized fork).

- Stop Homeassistant, using Hass.io developer tools, click `Services` and select `homeassistant.stop`;
- Clear the Homeassistant configuration located at `/usr/share/hassio/homeassistant`;
- Clone the IoT.Hass.Farm repository inside this folder;
- Run `./set-config.sh tank2` script to initialize configuration folder;
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

$ sudo ./set-config.sh tank2 pt

$ ls -l
-rw-r--r-- 1 root root        2 Jul 31 21:48 automations.yaml
-rwxr--r-- 1 root root     4123 Jul 31 22:22 configuration.yaml
-rw-r--r-- 1 root root      742 Jul 31 21:48 customize.yaml
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

After the boot, open the browser and enter the IP address of prototype followed by port 8123 to start the user interface. In the first use an user id and password will be required to create the admin account.
