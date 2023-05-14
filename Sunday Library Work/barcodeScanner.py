import cv2
from pyzbar import pyzbar
from button import Button

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
            # return the bounding box of the barcode
    return frame

def main():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()

    button = Button(25)  # Use the appropriate GPIO pin number for your setup

    while ret:
        ret, frame = camera.read()

        if button.is_pressed():
            camera.open(0)

        if button.is_double_pressed():
            if camera.isOpened():
                camera.release()

        frame = read_barcodes(frame)
        cv2.imshow('Real Time Barcode Scanner', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    if camera.isOpened():
        camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
