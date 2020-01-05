# iGrill Gateway
With this code you can monitor your iGrill_V2 (RPi Zero,1,2,3,4) and publish the messages to a MQTT Message Broker.

The code is based on the iGrill code from Bjoernhoefer (https://github.com/bjoernhoefer/igrill)


## Installation

### Manual
- Clone this repo with ( git clone https://github.com/Imperial-Guard/iGrill_Gateway.git )
- sudo mv Igrill_Gateway /opt

- Turn on the iGrill and scan with (hcitool lescan) for the bluetooth Address

- cd /opt/Igrill_Gateway/
- sudo nano monitor_igrill_v2.py (Change ADDRESS = 'XX:XX:XX:XX:XX:XX' and mqtt_server = "127.0.0.1") 
- Configure with config below.
- Restart Home-Assistant.

- cd /lib/systemd/system/
- ls

- sudo nano igrill.service

	Create File or Edit File
	sudo nano igrill.service

	[Unit]
	Description=igrill MQTT service
	After=network.target

	[Service]
	Type=simple
	Restart=always
	RestartSec=2
	ExecStart=/usr/bin/python /opt/Igrill_Gateway/monitor_igrill_v2.py

	[Install]
	WantedBy=multi-user.target

- sudo systemctl daemon-reload && systemctl enable igrill && systemctl start igrill
- sudo reboot

## Usage
To add the sensors in Home Assistant ad the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry

sensor:
- platform: mqtt  
  state_topic: garden/sensor/0002/igrill_gateway/probe1
  availability_topic: "garden/sensor/0002/igrill_gateway/availability_probe1"
  payload_available: "yes"
  payload_not_available: "no"
  value_template: "{{  value | round(1) }}"
  name: "Temperatuur Probe 1" 
  unit_of_measurement: "°C" 
  qos: 0
  entity_namespace: igrill  

- platform: mqtt  
  state_topic: garden/sensor/0002/igrill_gateway/probe2
  availability_topic: "garden/sensor/0002/igrill_gateway/availability_probe2"
  payload_available: "yes"
  payload_not_available: "no"
  value_template: "{{  value | round(1) }}"
  name: "Temperatuur Probe 2" 
  unit_of_measurement: "°C" 
  qos: 0
  entity_namespace: igrill  

- platform: mqtt  
  state_topic: garden/sensor/0002/igrill_gateway/probe3
  availability_topic: "garden/sensor/0002/igrill_gateway/availability_probe3"
  payload_available: "yes"
  payload_not_available: "no"
  value_template: "{{  value | round(1) }}"
  name: "Temperatuur Probe 3" 
  unit_of_measurement: "°C" 
  qos: 0
  entity_namespace: igrill  

- platform: mqtt  
  state_topic: garden/sensor/0002/igrill_gateway/probe4
  availability_topic: "garden/sensor/0002/igrill_gateway/availability_probe4"
  payload_available: "yes"
  payload_not_available: "no"
  value_template: "{{  value | round(1) }}"
  name: "Temperatuur Probe 4" 
  unit_of_measurement: "°C" 
  qos: 0
  entity_namespace: igrill  

- platform: mqtt  
  state_topic: garden/sensor/0002/igrill_gateway/battery
  availability_topic: "garden/sensor/0002/igrill_gateway/igrill_connected"
  payload_available: "yes"
  payload_not_available: "no"  
  name: "Accu Spanning"
  unit_of_measurement: "%"
  device_class: battery
  value_template: "{{ value | round(0) }}"
  qos: 0  
  entity_namespace: igrill
```
