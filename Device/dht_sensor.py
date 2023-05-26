import RPi.GPIO as GPIO
import Adafruit_DHT

class DHTSensor:
    def __init__(self, sensor_type, pin):
        self.sensor_type = sensor_type
        self.pin = pin

    def read_data(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor_type, self.pin)
        return humidity, temperature