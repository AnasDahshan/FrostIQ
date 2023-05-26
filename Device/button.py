import RPi.GPIO as GPIO

class Button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def is_pressed(self):
        if GPIO.input(self.pin) == GPIO.HIGH:
            print("Button pressed!")
            return True
        return False
