import paho.mqtt.client as mqtt

# MQTT broker details
broker_address = "localhost"
broker_port = 1883

# Topic to subscribe to
topic = "test"

# Callback function to handle received messages
def on_message(client, userdata, message):
    print("Received message:", str(message.payload.decode("utf-8")))

# Connect to MQTT broker
client = mqtt.Client()
client.connect(broker_address, broker_port)

# Set up message callback
client.on_message = on_message

# Subscribe to topic
client.subscribe(topic)

# Loop continuously to receive messages
client.loop_forever()
