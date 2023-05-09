import random
import time

class TemperatureSensor:
    def __init__(self):
        self.temperature = 0
    
    # Get method
    def get_temperature(self):
        self.temperature = random.uniform(0.0, 100.0) # Generates a random float between 0.0 and 10.0
        return self.temperature


    # def highTemp(temperature):
    #     if temperature > 40:
    #         #TODO Notify user....

temperature_sensor = TemperatureSensor()

while True:
    temperature = temperature_sensor.get_temperature()
    # highTemp(temperature)
    print(f"Temperature: {temperature}°C")
    time.sleep(2) # Sleep for 2 minutes
