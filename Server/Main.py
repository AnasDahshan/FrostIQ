import paho.mqtt.client as mqtt

# MQTT broker details
broker_address = "28d2c0c050044799bd9854cb365d4d4f.s2.eu.hivemq.cloud"
broker_port = 8883
username = "user_side"
password = "User1234"

# Topics
temperature_topic = "fridge/temperature"
light_topic = "fridge/light"
barcode_topic = "fridge/barcode"

# Define callback functions for MQTT client
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))
    # Subscribe to temperature, light and barcode topics
    client.subscribe(temperature_topic)
    client.subscribe(light_topic)
    client.subscribe(barcode_topic)

def on_message(client, userdata, message):
    #ToDO:


    print("Received message on topic "+message.topic+": "+str(message.payload))
    # Send to a database instead of printing it to the console..


# Connect to MQTT broker
client = mqtt.Client("UserClient")
client.username_pw_set(username, password)
client.tls_set()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port)

# Loop forever and handle incoming MQTT messages
print("Starting MQTT loop")
client.loop_forever()
