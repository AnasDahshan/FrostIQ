import paho.mqtt.client as mqtt

class MqttDevice:
    def __init__(self):
        # MQTT broker details
        self.broker_address = "localhost"
        self.broker_port = 1883
        self.client = mqtt.Client("RaspberryPi")
        self.status = False

    def signIn(self, username, password):
        if username == "device_u745" and password == "Frost1234":
            self.status = True
            # Connect client
            self.client.connect(self.broker_address, self.broker_port)
        else:
            print("Invalid Credentials")

    def signOut(self):
        # Disconnect from MQTT broker
        self.client.disconnect()
