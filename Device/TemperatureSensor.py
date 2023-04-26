import random
import time

class TemperatureSensor:
    def __init__(self):
        self.temperature = 0
    
    # Get method
    def get_temperature():
        #READIANG from sesor 
        temperature = random.uniform(0.0, 100.0) # Generates a random float between 0.0 and 10.0
        return temperature

