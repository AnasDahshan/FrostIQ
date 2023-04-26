import paho.mqtt.client as mqtt
import random
import time
from raspTemp import TemperatureSensor
from raspLight import LightSensor

# MQTT broker details
broker_address = "28d2c0c050044799bd9854cb365d4d4f.s2.eu.hivemq.cloud"
broker_port = 8883
username = "frostIQ"
password = "frostiq123"

# Topics
temperature_topic = "fridge/temperature"
light_topic = "fridge/light"
product_topic = "fridge/product"

# Connect to MQTT broker
client = mqtt.Client("FridgeClient")
client.username_pw_set(username=username, password=password)
client.tls_set()

client.connect(broker_address, broker_port)

# Continuously generate and publish random temperature and light readings
while True:
    temperature = TemperatureSensor.get_temperature()
    client.publish(temperature_topic, temperature)
    print("Published temperature:", temperature)

    # Generate random light reading between 0 and 1 (0=off, 1=on)
    light = LightSensor.is_light_on()
    # Publish light reading to MQTT broker
    client.publish(light_topic, light)
    print("Published light:", light)

    # # Generate random barcode number between 1000 and 9999
    # barcode = random.randint(1000, 9999)
    # # Publish barcode number to MQTT broker
    # client.publish(barcode_topic, barcode)
    # print("Published barcode:", barcode)

    # Wait for 5 seconds before generating next set of readings
    time.sleep(5)

# Disconnect from MQTT broker
client.disconnect()
