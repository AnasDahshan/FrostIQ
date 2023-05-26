import threading
import time 
class DHTSensorThread(threading.Thread):
    def __init__(self, sensor, push_dht, is_camera_on):
        threading.Thread.__init__(self)
        self.sensor = sensor
        self.push_dht = push_dht
        self.is_camera_on = is_camera_on

    def run(self):
        while True:
            humidity, temperature = self.sensor.read_data()
            # Process the sensor data as needed

            # Print temperature and humidity to the console
            print('Temperature: {0:0.1f}°C'.format(temperature))
            print('Humidity: {0:0.1f}%'.format(humidity))

            self.push_dht.push_dht_data_firebase(temperature, humidity)

            time.sleep(10)  # Delay for 10 seconds