import threading
import time
import RPi.GPIO as GPIO

class LDRSensorThread(threading.Thread):
    def __init__(self, sensor, push_ldr, buzzer, is_camera_on):
        threading.Thread.__init__(self)
        self.sensor = sensor
        self.push_ldr = push_ldr
        self.buzzer = buzzer
        self.is_camera_on = is_camera_on
        self.light_on_start_time = None  # Variable to store the start time of light being on
        self.buzzer_active = False  # Flag to indicate if the buzzer is currently active

    def buzz_repeatedly(self):
        while self.buzzer_active:
            self.buzzer.Buzz()  # Sound the warning buzzer
            time.sleep(0.2)

    def run(self):
        while True:
            light_status = self.sensor.read_data()

            # Print light status to the console
            print('Light Status:', light_status)

            if light_status == 0:
                if self.light_on_start_time is None:
                    self.light_on_start_time = time.time()  # Store the start time of light being on
                else:
                    current_time = time.time()
                    elapsed_time = current_time - self.light_on_start_time
                    if elapsed_time >= 10 and not self.buzzer_active:
                        self.buzzer_active = True  # Activate the buzzer
                        # Start the buzzer buzzing thread
                        buzzer_thread = threading.Thread(target=self.buzz_repeatedly)
                        buzzer_thread.start()
            else:
                self.light_on_start_time = None  # Reset the start time if the light is off
                self.buzzer_active = False  # Deactivate the buzzer

            self.push_ldr.push_ldr_data_firebase(light_status)

            time.sleep(1)  # Delay for 10 seconds

