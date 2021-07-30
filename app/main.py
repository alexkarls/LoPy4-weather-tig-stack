# Core libraries
import hashlib
import json
import time
import sys

# Pycom modules: https://docs.pycom.io/firmwareapi/pycom/
import machine
import ubinascii

# Libraries in the "lib" folder
from mqtt import MQTTClient
from dht import DHT

# Self-made "libraries"
from light_sensor import LightSensor
from util import heartbeat

heartbeat(False)

# Config contains sensitive information used in the app
with open('config.json') as f:
    config = json.load(f)

### MQTT related code
### Inspired by: https://github.com/iot-lnu/applied-iot/blob/master/network-examples/ccs811-bmp180-dht22-MQTT/main.py

# MQQT constants
TOPIC_PUB = 'ak223ke/devices/weather/'
TOPIC_SUB = 'ak223ke/devices/weather/control'
BROKER_URL = 'mqtt.iotlab.dev'
CLIENT_NAME = ubinascii.hexlify(hashlib.md5(machine.unique_id()).digest()) # create a md5 hash of the pycom WLAN mac

# Note: Broker has QoS set to 0 so callback not implemented
client = MQTTClient(CLIENT_NAME, BROKER_URL, user=config['user_mqtt'], password=config['pass_mqtt'])
client.connect()

### Sensor related code

# Sensor constants
DHT_SENSOR_PIN = 'P23'
LIGHT_SENSOR_PIN = 'P20'
SLEEP_INTERVAL_SECONDS = 600

# DHT sensor type 0 (argument) = DHT11
dht_sensor = DHT(machine.Pin(DHT_SENSOR_PIN, mode=machine.Pin.OPEN_DRAIN), 0)
light_sensor = LightSensor(LIGHT_SENSOR_PIN)

# Wait to make sure classes / device is ready
time.sleep(2)

def send_data():
  dict = {'home_sensor_1': {}}
  dht_result = dht_sensor.read()
  light_result = light_sensor.read()
  if (dht_result.is_valid()):
      dict['home_sensor_1'].update({ 'temperature': dht_result.temperature })
      dict['home_sensor_1'].update({ 'humidity': dht_result.humidity })
  else:
    raise Exception('DHT Error: ', dht_result.error_code)
  # No error checking implemented for the light sensor
  dict['home_sensor_1'].update({ 'light': light_result})
  # Publish the dictionary over MQTT as JSON
  print(dict)
  client.publish(TOPIC_PUB, json.dumps(dict))

# Exception loop, exit on 3600 attempts (1 hour)
def exception_loop():
  for i in range(3600):
    try: 
      send_data()
      return # Return on success
    except Exception as e:
      print('Error: ', e)
    finally:
      time.sleep(1)
  # Exit on failed retries
  sys.exit()

# Main loop
while True:
  try:
    send_data()
  except Exception as e:
    print('Error: ', e)
    exception_loop()
  finally: 
    time.sleep(SLEEP_INTERVAL_SECONDS)

