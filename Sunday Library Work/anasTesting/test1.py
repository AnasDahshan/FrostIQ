import cv2
from pyzbar import pyzbar
from time import sleep
import RPi.GPIO as GPIO

class Button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    def is_pressed(self):
        if GPIO.input(self.pin) == GPIO.HIGH:
            return True
        return False

    def is_double_pressed(self):
        if self.is_pressed():
            sleep(0.1)
            if self.is_pressed():
                return True
        return False

def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        # 1
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # 2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        # 3
        with open("barcode_result.txt", mode='w') as file:
            file.write("Recognized Barcode: " + barcode_info)

    return frame

def main():
    button = Button(23)  # GPIO pin 23 for the button
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    is_camera_on = False  # Flag to keep track of camera state

    while ret:
        if button.is_double_pressed():
            is_camera_on = not is_camera_on  # Toggle camera state

        if is_camera_on:
            ret, frame = camera.read()
            frame = read_barcodes(frame)
            cv2.imshow('Real Time Barcode Scanner', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
