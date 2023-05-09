import paho.mqtt.client as mqtt
import time

# MQTT broker details
broker_address = "localhost"
broker_port = 1883

# Topic to publish to
topic = "test"

# Connect to MQTT broker
client = mqtt.Client()
client.connect(broker_address, broker_port)

# Publish message to MQTT broker
while True:
	message = "Hello, MQTT!"
	client.publish(topic, message)
    # Wait for 5 seconds before generating next set of readings
	time.sleep(5)

# Disconnect from MQTT broker
client.disconnect()

