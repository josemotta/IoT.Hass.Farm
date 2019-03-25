![Travis branch](https://api.travis-ci.org/josemotta/IoT.Hass.Farm.svg?branch=master)

# Iot.Hass.Farm

**An IoT hass farm for supervisory, control & data acquisition systems.**

## Introduction

This article intends to combine cheap CPUs and open source microservices to develop an architecture for distributed supervisory and control systems.

## SCADA (Supervisory Control and Data Acquisition)

The SCADA architecture has functional levels layered as a pyramid that has been used to power solutions for home/office/industrial automation. Since the '70s, the SCADA concept has pioneered the ability to perform supervisory operations over a variety of other proprietary devices. 

#scada picture

As shown in the diagram, the lowest level interfaces with the process, maybe a home/office/factory for example.  The higher levels communicate to gather information from lower levels, analyze the data and evaluate the decisions to be made, eventually sending down commands to adjust the process behavior.

Today, IoT solutions face similar challenges concerning the development of home automation systems. Usually, a single computer solution may grow with more CPU power, eventually restricted by some proprietary technologies that connect the devices. Another option is going for an open source distributed architecture, based on microservices running on small CPUs, tied through an API. 

The following project shows an IoT architecture based on Raspberry Pi hardware and Home Assistant software installed on a Linux environment that uses Docker containers to launch several microservices on each node.

## Water Tanks Project

The picture describes a typical process that pumps water from well and fills the big water storage placed on a high tower. The plumbing connects to water points located on the near buildings, equipped with secondary water tanks that should also be monitored.

![](https://i.imgur.com/4fRKJ5g.jpg)

Since the tanks may be distributed in a wide area, the distributed architecture dedicates a node to get data from each tank, including water level, temperature, humidity, and luminance. 

![](https://i.imgur.com/v9vMVrP.jpg)

The picture shows the sensor located at the top of the tank, pointing down to the water. The distance to the water allows calculating the tank water level and consequently the water volume stored in the tank. The sonar technology has been frequently used for this task, the HC-SR04 is a popular example. In this project, a different option will replace sound with light. The STMicroelectronics VL53L1X "time of flight sensor" is equipped with an invisible laser to measure distances with millimeter resolution,  get the full specs on the product page.

![](https://i.imgur.com/E2FPbNT.jpg)

The tanks nodes themselves are not enough to calculate the total water in the system since they only handle local information about each tank. As shown in the picture, a second level is created for a supervisor node that collects information from all tanks. MQTT streaming generated at each tank publishes the tank variables that should be monitored. The preliminary user interface, also located at the tank supervisor, shows information from all tanks.

The system shows a couple of layers that are scalable to monitor all tank data and are smart enough to handle eventual local decisions.

The Raspberry Pi ZeroW was used to measure the water level and other environmental data from water tanks. Code from a  Python 2 library was upgraded to Python 3 in order to be applied to the new "Time of Flight" platform for Home Assistant.


## Conclusions

Nonini ni no nin nonoi nino Nonini no nin nonoi nino Nonini no nin nonoi nino Nonini no nin nonoi nino Noni nino Nonini no nin noi no nin nonoi nino Nonini no nin nonoi nino Nonini no nin nonoi nino Nonini no nin nonoi nino Noni nino Nonini no nin no o nin nonoi nino, Nonini no nin nonoi nino. Nonini no nin nonoi nino Nonini no nin nonoi nino Nonini no nin nonoi nino noi nino Nonini no nin nonoi nino Nonini no nin nonoi nino Nonini no nin nonoi nino Nonini no nin nonoi nino Noninnoi nino.

Have fun with your IoT initiative!

*Did you like it? Please click the :star: on the top!*