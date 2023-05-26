import threading
import time
class CameraThread(threading.Thread):
    def __init__(self, camera, barcode_reader, push_image, push_barcode, is_camera_on, scanned_barcodes):
        threading.Thread.__init__(self)
        self.camera = camera
        self.barcode_reader = barcode_reader
        self.push_image = push_image
        self.push_barcode = push_barcode
        self.is_camera_on = is_camera_on
        self.scanned_barcodes = scanned_barcodes

    def run(self):
        while True:
            if self.is_camera_on:
                # Read frame from the camera
                ret, frame = self.camera.read()
                barcode_data, frame = self.barcode_reader.read_barcodes(frame)
                if barcode_data:
                    self.scanned_barcodes.put(barcode_data)
                cv2.imshow("Real Time Barcode Scanner", frame)

            time.sleep(0.01)  # Delay for a short interval