import RPi.GPIO as GPIO
import time

class Buzzer:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def Buzz(self):
        GPIO.output(self.pin, True)
        time.sleep(0.2)
        GPIO.output(self.pin, False)

