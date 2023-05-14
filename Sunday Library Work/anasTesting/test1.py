import cv2
from pyzbar import pyzbar
import RPi.GPIO as GPIO
import json

class Button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def is_pressed(self):
        if GPIO.input(self.pin) == GPIO.HIGH:
            return True
        return False

def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    barcode_list = []
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        barcode_list.append(barcode_info)
    
    return frame, barcode_list

def save_barcodes(barcode_list):
    with open("ScannedBarcodes.json", "a") as file:
        for barcode in barcode_list:
            json.dump({"Barcode": barcode}, file)
            file.write("\n")

def main():
    buttonOn = Button(23)  # GPIO pin 23 for the camera on button
    buttonOff = Button(24)  # GPIO pin 24 for the camera off button
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    is_camera_on = False  # Flag to keep track of camera state
    prev_button_on_state = False
    prev_button_off_state = False
    scanned_barcodes = []  # List to store scanned barcode values

    while ret:
        if not prev_button_on_state and buttonOn.is_pressed():
            is_camera_on = not is_camera_on  # Toggle camera state
            if is_camera_on:
                print("Camera is on")
            else:
                print("Camera is off")

        if not prev_button_off_state and buttonOff.is_pressed():
            is_camera_on = False
            print("Camera is off")
            if scanned_barcodes:
                save_barcodes(scanned_barcodes)
                scanned_barcodes = []

        prev_button_on_state = buttonOn.is_pressed()
        prev_button_off_state = buttonOff.is_pressed()

        if is_camera_on:
            ret, frame = camera.read()
            frame, barcode_list = read_barcodes(frame)
            scanned_barcodes.extend(barcode_list)
            cv2.imshow('Real Time Barcode Scanner', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
