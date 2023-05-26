import cv2
import os
import time
import threading
import firebase_admin
from firebase_admin import credentials, firestore
from button import Button
from buzzer import Buzzer
from barcode_reader import BarcodeReader
from push_image import PushImage
from push_barcode import PushBarcode
from dht_sensor import DHTSensor
from ldr_sensor import LDRSensor
from dht_sensor_thread import DHTSensorThread
from ldr_sensor_thread import LDRSensorThread
from camera_thread import CameraThread
import Adafruit_DHT
import RPi.GPIO as GPIO
from queue import Queue

class PushLDRFirebase:
    def __init__(self, db):
        self.db = db

    def push_ldr_data_firebase(self, light_status):
        doc_ref = self.db.collection('light').document()
        doc_ref.set({
            'light_status': light_status,
            'timestamp': firestore.SERVER_TIMESTAMP
        })

class PushDHTFirebase:
    def __init__(self, db):
        self.db = db

    def push_dht_data_firebase(self, temperature, humidity):
        doc_ref = self.db.collection('temperature').document()
        doc_ref.set({
            'temperature': temperature,
            'humidity': humidity,
            'timestamp': firestore.SERVER_TIMESTAMP
        })

def main():
    global scanned_barcodes_list

    # Initialize button instances
    buttonOn = Button(22)
    buttonOff = Button(27)
        # Create and start the camera thread
    barcode_set = set()
    scanned_barcodes = Queue()

    # Initialize camera
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()

    is_camera_on = False
    button_pressed_time = 0
    is_picture_taken = False
    # scanned_barcodes = set()

    # Create "images" folder if it doesn't exist
    if not os.path.exists("images"):
        os.makedirs("images")

    # Initialize Firebase app and Firestore client using the service account key
    cred = credentials.Certificate("/home/onyx/Downloads/frost-iq-firebase-adminsdk-ooc0g-e7756d0f91.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    barcode_reader = BarcodeReader(18, scanned_barcodes)
    push_image = PushImage(db)
    push_barcode = PushBarcode(db)
    push_ldr = PushLDRFirebase(db)
    push_dht = PushDHTFirebase(db)

    # Set sensor types and GPIO pins
    dht_sensor = DHTSensor(Adafruit_DHT.DHT11, 23)
    ldr_sensor = LDRSensor(24)

    # Configure GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ldr_sensor.pin, GPIO.IN)

    ldr_last_read_time = time.time()
    dht_last_read_time = time.time()

    # Create and start sensor threads
    dht_thread = DHTSensorThread(dht_sensor, push_dht, is_camera_on)
    ldr_thread = LDRSensorThread(ldr_sensor, push_ldr, is_camera_on)
    dht_thread.start()
    ldr_thread.start()



    camera_thread = CameraThread(camera, barcode_reader, push_image, push_barcode, is_camera_on, scanned_barcodes)
    camera_thread.start()

    while ret:
        if is_camera_on:
            # Read frame from the camera
            ret, frame = camera.read()
            frame = barcode_reader.read_barcodes(frame)
            cv2.imshow("Real Time Barcode Scanner", frame)

        # Check for button presses
        if buttonOn.is_pressed():
            if not is_camera_on:
                if time.time() - button_pressed_time >= 4:  # Minimum 4 seconds between each picture
                    is_camera_on = True
                    print("Camera turned on")
                    button_pressed_time = time.time()
            elif time.time() - button_pressed_time >= 4 and not is_picture_taken:
                # Take a picture and save it
                image_path = os.path.join("images", f"image{time.time()}.jpg")
                cv2.imwrite(image_path, frame)
                print(f"Image saved: {image_path}")
                buzzer = Buzzer(18)  # Initialize the buzzer
                buzzer.Buzz()  # Buzz the buzzer
                is_picture_taken = True

                # Reset the flag after the picture is taken
                is_picture_taken = False

        if buttonOff.is_pressed():
            if is_camera_on:
                is_camera_on = False
                print("Camera turned off")
                is_picture_taken = False  # Reset the flag
                image_files = os.listdir("images")
                for image_file in image_files:
                    image_path = os.path.join("images", image_file)
                    push_image.push_image_firebase(image_path)
                    os.remove(image_path)
                    print(f"Image uploaded to Firebase Storage: {image_file}")
                    print("Image deleted: ", image_file)

                if len(image_files) > 0:
                    print("All images uploaded to Firebase Storage")

                while not scanned_barcodes.empty():
                    barcode = scanned_barcodes.get()
                    if barcode not in barcode_set:
                        push_barcode.push_barcode_firebase(barcode)
                        barcode_set.add(barcode)

                print("Scanned Barcodes: ", barcode_set)

                barcode_set.clear()
                while not scanned_barcodes.empty():
                    scanned_barcodes.get()

                print("All barcodes uploaded to Firebase Storage")

        if cv2.waitKey(1) & 0xFF == 27:
            break

        # Delay for a certain interval (e.g., 1 second) before reading again
        #time.sleep(1)

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
