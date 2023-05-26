import cv2
from pyzbar import pyzbar
from buzzer import Buzzer
from queue import Queue

class BarcodeReader:
    def __init__(self, buzzer_pin, scanned_barcodes):
        self.buzzer = Buzzer(buzzer_pin)
        self.scanned_barcodes = scanned_barcodes

    def read_barcodes(self, frame):
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y, w, h = barcode.rect
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)

            print("Scanned Barcode: " + barcode_info)
            self.buzzer.Buzz()
            self.scanned_barcodes.put(barcode_info)

        return frame
    
