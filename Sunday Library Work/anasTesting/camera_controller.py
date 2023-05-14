import cv2
from button import Button
from barcode_scanner import BarcodeScanner

class CameraController:
    def __init__(self, camera_index):
        self.camera = cv2.VideoCapture(camera_index)
        self.is_camera_on = False
        self.button_on = Button(23)  # GPIO pin 23 for the camera on button
        self.button_off = Button(24)  # GPIO pin 24 for the camera off button

    def toggle_camera_state(self):
        self.is_camera_on = not self.is_camera_on

    def process_frames(self):
        ret, frame = self.camera.read()
        barcode_scanner = BarcodeScanner()

        while ret:
            if self.button_on.is_pressed():
                self.toggle_camera_state()
                if self.is_camera_on:
                    print("Camera is on")
                else:
                    print("Camera is off")

            if self.button_off.is_pressed():
                self.is_camera_on = False
                print("Camera is off")
                if barcode_scanner.scanned_barcodes:
                    barcode_scanner.save_barcodes()
                    barcode_scanner.scanned_barcodes = set()

            if self.is_camera_on:
                ret, frame = self.camera.read()
                frame, barcode_set = barcode_scanner.read_barcodes(frame)
                cv2.imshow('Real Time Barcode Scanner', frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        self.camera.release()
        cv2.destroyAllWindows()
