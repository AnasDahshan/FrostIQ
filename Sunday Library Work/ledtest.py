import RPi.GPIO as GPIO
from time import sleep
from button import Button

LED_PIN = 18
BUTTON_PIN = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

button = Button(BUTTON_PIN)

led_state = False  # Variable to track LED state

try:
    while True:
        # Check button state
        if button.is_pressed():
            # Button pressed once
            if not led_state:
                GPIO.output(LED_PIN, GPIO.HIGH)
                led_state = True
                print("LED turned on")
            # Button pressed twice
            else:
                GPIO.output(LED_PIN, GPIO.LOW)
                led_state = False
                print("LED turned off")

        # Delay for smooth execution
        sleep(0.1)

except KeyboardInterrupt:
    # Cleanup GPIO on program exit
    GPIO.cleanup()
