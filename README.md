![Travis branch](https://api.travis-ci.org/josemotta/IoT.Hass.Farm.svg?branch=master)

# IoT.Hass.Farm

**An IoT hass farm for supervisory, control & data acquisition systems.**

## Introduction

This project intends to combine cheap CPUs and open source microservices to develop an architecture for distributed supervisory and control systems.

### SCADA (Supervisory Control and Data Acquisition)

The [SCADA architecture](https://en.wikipedia.org/wiki/SCADA) has functional levels layered as a pyramid that have been used to evolve solutions for home/office/industrial automation. Since the '70s, the SCADA concept has pioneered the ability to perform supervisory operations over a variety of other proprietary devices. 

![](https://i.imgur.com/dO70VcW.jpg)

As shown in the diagram, the lowest level interfaces with the process, maybe a home/office/factory for example.  The higher levels communicate to gather information from lower levels, analyze the data and evaluate the decisions to be made, eventually sending down commands to adjust the process behavior.

Today, IoT solutions face similar challenges concerning the development of home automation systems. Usually, a single computer solution may grow with more CPU power, eventually restricted by some proprietary technologies that connect the devices. Another option is going for an open source distributed architecture, based on microservices running on small CPUs, tied through APIs. 

## Summary

This project develops a distributed IoT architecture based on Raspberry Pi hardware and Home Assistant (HA) software. The system is installed on a Linux environment with Docker containers launching several microservices on each node.

There are different types of IoT devices cooperating in a single system. Each device is considered a node with its own HA configuration, automation and user interface scripts. The nodes share common Home Assistant files, like customizations, groups and secrets. 

A couple questions arise when we start designing the system:

- How big should be the CPU for each node?
- How each node connects to power and communication?
- How many wires are necessary to bring node to life?

Table below classifies the three nodes created for this application.

![](https://i.imgur.com/8XzDA8M.png)

- `_tank`: This node uses a wire to power a Raspberry Pi Zero-W device equipped with Wifi communication.
- `_pump`: This node changes CPU to Raspberry Pi 3B+ with a PoE (Power over Ethernet) Hat that allows both power and communication over a twisted-pair cable.
- `_super`: This node uses a couple wires: a cable for power and another Ethernet twisted-pair with RJ-45 connector to connect the Raspberry Pi 3B+ to LAN. 

## Water Process

The picture describes a typical process that pumps water from well and fills the big water storage placed on a high tower. The plumbing connects to water points located on the near buildings, equipped with secondary water tanks that should also be monitored.

![](https://i.imgur.com/4fRKJ5g.jpg)

### Tank node

Since several tanks may exist in a wide area, the proposed distributed architecture dedicates a node to get data from each tank, including water level, temperature, humidity, and luminance. 

![](https://i.imgur.com/V5eEZaI.jpg)

The picture shows the level sensor located at the top of the tank, pointing down towards water. The distance to the water allows calculating the water level and consequently the volume stored in the tank. The sonar technology has been frequently used for this task, the HC-SR04 is a popular example. In this project, a different option replaces sound with light.

The component chosen here is the STMicroelectronics VL53L1X "time of flight sensor", equipped with an invisible laser to measure distances with millimeter resolution. Please check the [full specs on the product page](https://www.st.com/en/imaging-and-photonics-solutions/vl53l1x.html) and the available [breakout](https://www.sparkfun.com/products/14722) shown below.

![](https://i.imgur.com/csxnBtA.jpg)

### Supervisor node

The tanks nodes themselves are not enough to calculate the total water in the system since they only handle local information about each tank. As shown in the diagram below, a second level is created for a supervisor node that collects information from all tanks.

![](https://i.imgur.com/E2FPbNT.jpg)

MQTT streaming generated at each tank node publishes the variables that should be monitored. A preliminary user interface is located at the tank supervisor, showing information from all tanks. This system may be easily scaled for many tanks and is smart enough to handle simple decisions.

The Raspberry Pi Zero-W is a cheap and powerful choice to measure the water level and other environmental data from water tanks. The source code from an available Python 2 library should be upgraded to Python 3 in order to create a new "Time of Flight" platform for Home Assistant.

The Raspberry Pi 3B was used at the supervisor node since further processing is expected in the near future. For this project, in order to make comparisons with tank data, the supervisor also has sensors to collect the ambient temperature, humidity, and luminance.

### Pump node

This node gets info from pumps to inform how much water is being moved to the tanks. We know that a lot of electromagnetic interference exists near pumps, and definitely this is not healthful to computer CPUs. In order to keep node connections far from this wild environment, power and communication will be provided by the Power over Ethernet technology. A RPI PoE HAT providing 5V DC/2.5A  from the RJ-45 network port (PoE IEEE 802.3af) will be used to power the Raspberry 3B+ CPU.

A hall-effect sensor generates an analog voltage proportional to each pump power current. A analog to digital converter will keep track of analog values in order to evaluate the pumps performance. 

### Microservices

The running containers at tank and supervisor nodes are shown below, using the `docker ps` with an option for pretty-printing the command output.

#### Tank node

The `tank node` has three microservices running: the Hass.io supervisor, the Homeassistant software and the Samba add-on that allows network access to configuration files.

```
$ ssh pi@cast
pi@cast's password:
Linux cast 4.14.71+ #1145 Fri Sep 21 15:06:38 BST 2018 armv6l
...
Last login: Fri Mar 29 22:21:27 2019 from 192.168.20.113

pi@cast:~ $ docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Status}}"
CONTAINER ID        IMAGE                                     STATUS
d2ff42ec7739        homeassistant/armhf-hassio-supervisor     Up 2 hours
22ef93868dbf        homeassistant/raspberrypi-homeassistant   Up 3 days
7f761d6a8dbd        homeassistant/armhf-addon-samba           Up 3 days
```
The Hass.io setup for tank node is shown below:

![](https://i.imgur.com/KssPfcg.jpg)

#### Supervisor node

The `supervisor node` has four microservices running: the Hass.io supervisor, the Homeassistant software, the MQTT server, and the Samba add-on that allows network access to configuration files. 

```
$ ssh pi@lava
pi@lava's password:
Linux lava 4.14.71-v7+ #1145 SMP Fri Sep 21 15:38:35 BST 2018 armv7l
...
Last login: Tue Mar 26 22:08:38 2019 from 192.168.20.113

pi@lava:~ $ docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Status}}"
CONTAINER ID        IMAGE                                      STATUS
4f058070fb47        homeassistant/raspberrypi3-homeassistant   Up 3 days
bff95bb5169c        homeassistant/armhf-addon-samba            Up 4 days
ce8ab55c04ef        homeassistant/armv7-addon-mosquitto        Up 4 days
d3ae6c4ceeff        homeassistant/armhf-hassio-supervisor      Up 4 days
```

The Hass.io setup for supervisor node is shown below:

![](https://i.imgur.com/tjMK9EV.jpg)

## Conclusions

The supervisor panel shown below contains water level and environmental data collected from a single tank. The delta temperature is calculated for each tank, based on the difference between data collected from it and the "normal" temperature registered by supervisor sensors. This way, an alarm for unexpected temperature in the tank may be raised, demonstrating the typical behavior from higher levels nodes in the SCADA architecture.  

![](https://i.imgur.com/no17Gds.jpg)

Further details about this project are published separately for each node. Please check:

- [Tank node](https://github.com/josemotta/IoT.Hass.Farm/tree/master/_tank)
- [Supervisor node](https://github.com/josemotta/IoT.Hass.Farm/tree/master/_super)
- [Pump node](https://github.com/josemotta/IoT.Hass.Farm/tree/master/_pump)

#### Known issues

##### BH1750 and HTU21D sensors fail at RPI0 linux-armv6l-3.7

Note: This issue is already solved, please update to the latest version (HA 0.96.5 or greater).

After updating HA to 0.95.4, the BH1750 and HTU21D sensors failed to install. Looks like ha container is trying to build wheels on the fly but gcc support is missing. In this same system works fine a Time of Flight VL53L1X laser distance detector that also uses I2C. Rolling back to HA version 0.92.2 everything works fine. Follow these [instructions to change version](https://community.home-assistant.io/t/0-86-1-broke-virtually-everything/94218/17?u=hads514). More details in the [closed issue](https://github.com/home-assistant/home-assistant/issues/24926 "BH1750 and HTU21D sensors fail at RPI0 linux-armv6l-3.7 #24926") at Homeassistant repo.

Have fun with your IoT initiative!

*Did you like it? Please click the :star: on the top!*