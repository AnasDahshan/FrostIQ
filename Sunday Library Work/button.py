from time import sleep
import RPi.GPIO as GPIO

class Button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def is_pressed(self):
        if GPIO.input(self.pin) == GPIO.HIGH:
            return True
        return False

    def is_double_pressed(self):
        if self.is_pressed():
            sleep(0.1)
            if self.is_pressed():
                return True
        return False
