import random
import time
from datetime import datetime
from TemperatureSensor import TemperatureSensor
from LightSensor import LightSensor
from MqttDevice import MqttDevice


# MQTT broker details
username = input("Enter MQTT broker username: ")
password = input("Enter MQTT broker password: ")

# Topics
temperature_topic = "fridge/temperature"
light_topic = "fridge/light"
product_topic = "fridge/product"

# Instantiate MqttComm object
mqtt_client = MqttDevice()

# Connect to MQTT broker
mqtt_client.signIn(username, password)

# Continuously generate and publish random temperature and light readings
while (mqtt_client.status):
    temperature = TemperatureSensor.get_temperature()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mqtt_client.client.publish(temperature_topic, f"{timestamp} - {temperature}")
    print("Published temperature:", temperature)

    # Generate random light reading between 0 and 1 (0=off, 1=on)
    light = LightSensor.is_light_on()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Publish light reading to MQTT broker
    mqtt_client.client.publish(light_topic, f"{timestamp} - {light}")
    print("Published light:", light)

    # Wait for 5 seconds before generating next set of readings
    time.sleep(5)

# Disconnect from MQTT broker
mqtt_client.signOut()
