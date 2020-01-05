import json
import time
import paho.mqtt.client as mqtt
import logging
import signal
from bluepy.btle import BTLEException

from igrill import IGrillV2Peripheral

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

ADDRESS = 'D4:81:CA:23:5B:98'
# DATA_FILE = '/tmp/igrill.json'
INTERVAL = 5
RECONNECT_INTERVAL=10

mqtt_server = "127.0.0.1"
# MQTT Section
client = mqtt.Client()
client.connect(mqtt_server, 1883, 60)
client.loop_start()

class TimeoutError(Exception):
  pass


def timeout(func, args=(), kwargs={}, timeout_duration=1):

    def handler(signum, frame):
      raise TimeoutError()

    # set the timeout handler
    signal.signal(signal.SIGALRM, handler) 
    signal.alarm(timeout_duration)

    myExc=None
    try:
        result = func(*args, **kwargs)
    except TimeoutError as exc:
      raise
    finally:
        signal.alarm(0)

    return result
def get_values(periph):

#this method gets the values from the device, but may hang if device suddenly disconnects
    return (periph.read_temperature(), periph.read_battery())

def connect_igrill(addr):
  while True:
    try:
      return IGrillV2Peripheral(addr)
    except:
      log.warn("Failed to connect, will retry")
      time.sleep(RECONNECT_INTERVAL)


if __name__ == '__main__':
 periph = connect_igrill(ADDRESS)
 last_online_status=True
 probe_status={}
 client.publish("garden/sensor/0002/igrill_gateway//igrill_connected", "yes", retain=True)
 while True:
  while True:
    try:
     # temperature=periph.read_temperature()
     (temperature, battery) = timeout(get_values, (periph, ), timeout_duration=10)
     break
    except (BTLEException, TimeoutError):
      log.warn("Failed to get values", exc_info=True)
      if last_online_status:
        last_online_status=False
        client.publish("garden/sensor/0002/igrill_gateway/igrill_connected", "no", retain=True)
    periph = connect_igrill(ADDRESS)

  if not last_online_status:
    client.publish("garden/sensor/0002/igrill_gateway/igrill_connected", "yes", retain=True)
    last_online_status=True

  for i in temperature.keys():
    # Loop trough all temperature sensors
    if temperature[i] != 63536.0:
      if not probe_status.get(i):
        probe_status[i] = True
        client.publish("garden/sensor/0002/igrill_gateway/availability_probe{}".format(i), "connected", retain=True)
      client.publish("garden/sensor/0002/igrill_gateway/probe{}".format(i), temperature[i])
    elif probe_status.get(i, True):
      probe_status[i] = False
      client.publish("garden/sensor/0002/igrill_gateway/availability_probe{}".format(i), "disconnected", retain=True)

  client.publish("garden/sensor/0002/igrill_gateway/battery", battery)

  time.sleep(INTERVAL)

