import cv2
from pyzbar import pyzbar
from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(17)  # GPIO pin 17 for the buzzer

def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)

        # Beep the buzzer
        buzzer.on()
        sleep(0.5)  # Beep for 0.5 seconds
        buzzer.off()

        with open("barcode_result.txt", mode='w') as file:
            file.write("Recognized Barcode: " + barcode_info)

    return frame

def main():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
