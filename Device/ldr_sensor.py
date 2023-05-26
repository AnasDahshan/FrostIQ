import RPi.GPIO as GPIO
class LDRSensor:
    def __init__(self, pin):
        self.pin = pin

    def read_data(self):
        return GPIO.input(self.pin)
