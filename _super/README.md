## Supervisor node

The `tanks nodes` themselves are not enough to calculate the total water in the system, since they only handle local information about each tank. As shown in the diagram below, a second level is created for a `supervisor node` that collects information from a group of tanks.

![](https://i.imgur.com/E2FPbNT.jpg)


The Raspberry Pi 3B was used at the supervisor node since further processing is expected in the near future. For this project, in order to make comparisons with tank data, the supervisor also has sensors to collect the room temperature, humidity, and luminance.

The supervisor node gather information about a group of tanks, using an MQTT server that receive messages from all tanks under its supervision. For this project, the supervisor  node should collect sensors measurements about water level, temperature, humidity and luminance from each tank. Then, a MQTT streaming generated from a group of tanks are published to their  respective supervisor.

### Publish tank data

A couple information is necessary to configure Homeassistant in each tank, in order to publish tank data to supervisor:

- Its corresponding supervisor, defined at the MQTT broker definition.
- The data to be monitored, configured at `statestream` feature.

Please see the details below, extracted from the `configuration.yaml` file from the tank node:

	...

	# MQTT Broker (aka Mosquitto)
	mqtt:
	  broker: !secret mqtt_broker
	  client_id: slave
	  port: !secret mqtt_port
	  keepalive: 60
	  username: !secret mqtt_username
	  password: !secret mqtt_password
	
	mqtt_statestream:
	  base_topic: homeassistant
	  publish_attributes: true
	  publish_timestamps: true
	  include:
	    entities:
	      - sensor.tank_water_level
	      - sensor.tank_vl53l1x
	      - sensor.tank_bh1750
	      - sensor.tank_htu21d_humidity
	      - sensor.tank_htu21d_temperature
	...


### MQTT data flow

A Homeassistant automation guarantees that the entities are recreated at supervisor node, as soon as they arrive at MQTT server. Every time that the tank publishes a MQTT message, the  automation, edited for clarity below, recreates the corresponding entity at the supervisor node.

	- id: '1552680266680'
	  alias: mqtt_config_entity_creator_sensor
	  trigger:
	  - platform: mqtt
	    topic: homeassistant/sensor/#
	  condition:
	  - condition: template
	    value_template: "{{ trigger.topic.split('/')[3] == 'unit_of_measurement' }}"
	  action:
	  - service: mqtt.publish
	    data_template:
	      topic: "homeassistant/sensor/{{ trigger.topic.split('/')[2] }}/config"
	      payload: "{\"name\": \"{{ trigger.topic.split('/')[2]| replace('_', ' ') | title }}\",
	               \"unit_of_measurement\": \"{{ trigger.payload_json }}\",
                   \"state_topic\": \"homeassistant/sensor/{{ trigger.topic.split('/')[2] }}/state\"}"
	      retain: true



The MQTT.fx Client shows below the data published at supervisor node.

![](https://i.imgur.com/6kSw95L.jpg)

### User Interface

An user interface may be created at the tank supervisor, able to show information from their respective tanks. This system may be easily scaled for many tanks and is smart enough to handle simple decisions. The following panel example shows data collected from a single tank. 

![](https://i.imgur.com/hJGcEWW.jpg)

The delta temperature is calculated for each tank, based on the difference between data collected from it and the "normal" temperature registered by supervisor sensors. An alarm for unexpected temperature in the tank may be raised, demonstrating the typical behavior from higher levels nodes in the SCADA architecture. The experiment also shows below some history data, collected with normal daylight.

![](https://i.imgur.com/J0eIXSV.jpg)

As you can notice, at night there is no luminance interference and ToF technology has a better precision (less variance) on measurements results. You can also verify the difference between tank and supervisor sensors shown in this panel.





