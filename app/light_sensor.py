# Based on: https://github.com/iot-lnu/applied-iot/blob/master/sensor-examples/Photoresistor/main.py
from machine import ADC

class LightSensor:
    def __init__(self, pin: str):
        self._apin = ADC(bits=10).channel(attn=ADC.ATTN_11DB, pin = pin)

    def read(self):
        return self._apin()
