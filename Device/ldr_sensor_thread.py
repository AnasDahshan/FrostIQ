import threading
import time 
class LDRSensorThread(threading.Thread):
    def __init__(self, sensor, push_ldr, is_camera_on):
        threading.Thread.__init__(self)
        self.sensor = sensor
        self.push_ldr = push_ldr
        self.is_camera_on = is_camera_on

    def run(self):
        while True:
            light_status = self.sensor.read_data()

            # Print light status to the console
            print('Light Status:', light_status)

            self.push_ldr.push_ldr_data_firebase(light_status)

            time.sleep(10)  # Delay for 10 seconds