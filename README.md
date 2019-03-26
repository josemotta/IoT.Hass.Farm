![Travis branch](https://api.travis-ci.org/josemotta/IoT.Hass.Farm.svg?branch=master)

# IoT.Hass.Farm

**An IoT hass farm for supervisory, control & data acquisition systems.**

## Introduction

This article intends to combine cheap CPUs and open source microservices to develop an architecture for distributed supervisory and control systems.

### SCADA (Supervisory Control and Data Acquisition)

The [SCADA architecture](https://en.wikipedia.org/wiki/SCADA) has functional levels layered as a pyramid that has been used to evolve solutions for home/office/industrial automation. Since the '70s, the SCADA concept has pioneered the ability to perform supervisory operations over a variety of other proprietary devices. 

![](https://i.imgur.com/dO70VcW.jpg)

As shown in the diagram, the lowest level interfaces with the process, maybe a home/office/factory for example.  The higher levels communicate to gather information from lower levels, analyze the data and evaluate the decisions to be made, eventually sending down commands to adjust the process behavior.

Today, IoT solutions face similar challenges concerning the development of home automation systems. Usually, a single computer solution may grow with more CPU power, eventually restricted by some proprietary technologies that connect the devices. Another option is going for an open source distributed architecture, based on microservices running on small CPUs, tied through an API. 

The following project shows an IoT architecture based on Raspberry Pi hardware and Home Assistant software installed on a Linux environment that uses Docker containers to launch several microservices on each node.

## Water Tanks Process

The picture describes a typical process that pumps water from well and fills the big water storage placed on a high tower. The plumbing connects to water points located on the near buildings, equipped with secondary water tanks that should also be monitored.

![](https://i.imgur.com/4fRKJ5g.jpg)

### Tank node

Since several tanks may exist in a wide area, the proposed distributed architecture dedicates a node to get data from each tank, including water level, temperature, humidity, and luminance. 

![](https://i.imgur.com/V5eEZaI.jpg)

The picture shows the level sensor located at the top of the tank, pointing down towards water. The distance to the water allows calculating the tank water level and consequently the water volume stored in the tank. The sonar technology has been frequently used for this task, the HC-SR04 is a popular example. In this project, a different option will replace sound with light.

The component chosen here is the STMicroelectronics VL53L1X "time of flight sensor", equipped with an invisible laser to measure distances with millimeter resolution. Please check the [full specs on the product page](https://www.st.com/en/imaging-and-photonics-solutions/vl53l1x.html) and the [breakout option](https://www.sparkfun.com/products/14722) shown below.

![](https://i.imgur.com/csxnBtA.jpg)

### Supervisor node

The tanks nodes themselves are not enough to calculate the total water in the system since they only handle local information about each tank. As shown in the picture, a second level is created for a supervisor node that collects information from all tanks.

![](https://i.imgur.com/E2FPbNT.jpg)

MQTT streaming generated at each tank node publishes the variables that should be monitored. A preliminary user interface is located at the tank supervisor, showing information from all tanks. This system may be easily scaled for many tanks and is smart enough to handle simple decisions.

The Raspberry Pi Zero-W is a cheap and powerful choice to measure the water level and other environmental data from water tanks. Library code from an old Python 2 library should be upgraded to Python 3 in order to create a new "Time of Flight" platform for Home Assistant. The Raspberry Pi 3B was used for the supervisor node since further processing is expected in the near future.


## Conclusions

The details about this project are published separately for each node. Please check:

- Tank node
- Supervisor node

Have fun with your IoT initiative!

*Did you like it? Please click the :star: on the top!*