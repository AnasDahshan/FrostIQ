import paho.mqtt.client as mqtt
from MQTTBackend import MQTTBackend 


username = input("Enter MQTT broker username: ")
password = input("Enter MQTT broker password: ")

client = MQTTBackend()
client.signIn(username, password)

