import time
import random

class LightSensor:
    def __init__(self):
        self.light_on = False
    
    # Get method
    def is_light_on():
        light_on = random.choice([True, False]) # Randomly choose whether the light is on or off
        return light_on

# while True:
#     is_light_on()
#     time.sleep(60) # Sleep for 1 second
