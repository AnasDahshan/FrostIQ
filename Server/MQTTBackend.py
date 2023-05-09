import paho.mqtt.client as mqtt

class MQTTBackend:
    def __init__(self):
        self.broker_address = "localhost"
        self.broker_port = 1883
        self.temperature_topic = "fridge/temperature"
        self.light_topic = "fridge/light"
        self.barcode_topic = "fridge/barcode"
        self.client = mqtt.Client("Backend")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.status = False

    def signIn(self, username, password):
        if username == "server_u745" and password == "Frost1234":
            self.status = True
            # self.client.username_pw_set(username, password)
            self.connect()
            self.loop_forever()
        else:
            print("Invalid Credentials")

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code "+str(rc))
        # Subscribe to temperature, light and barcode topics
        client.subscribe(self.temperature_topic)
        client.subscribe(self.light_topic)
        client.subscribe(self.barcode_topic)

    def on_message(self, client, userdata, message):
        #ToDo:
        print("Received message on topic "+message.topic+": "+message.payload.decode())
        # Send to a database instead of printing it to the console..

    def connect(self):
        self.client.connect(self.broker_address, self.broker_port)

    def loop_forever(self):
        # Loop forever and handle incoming MQTT messages
        print("Starting MQTT loop")
        self.client.loop_forever()
