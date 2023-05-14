import cv2
from pyzbar import pyzbar
import RPi.GPIO as GPIO
import time


def read_barcodes(frame, buzzer_pin):
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
        with open("barcode_result.txt", mode='a') as file:
            file.write("Recognized Barcode: " + barcode_info + "\n")

        # Beep on buzzer
        GPIO.output(buzzer_pin, GPIO.HIGH)
        time.sleep(0.2)  # Adjust the sleep time to control the beep duration
        GPIO.output(buzzer_pin, GPIO.LOW)

    return frame


def main():
    buzzer_pin = 23  # Set the GPIO pin number for the buzzer
    button_pin = 18  # Set the GPIO pin number for the button

    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame, buzzer_pin)
        cv2.imshow('Real Time Barcode Scanner', frame)

        # Check if the button is pressed
        if GPIO.input(button_pin) == GPIO.LOW:
            print("Button Pressed!")
            # Add code to turn on the camera here

        if cv2.waitKey(1) & 0xFF == 27:
            break

    camera.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()


if __name__ == '__main__':
    main()
