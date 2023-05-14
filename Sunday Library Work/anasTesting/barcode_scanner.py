import cv2
from pyzbar import pyzbar
import json

class BarcodeScanner:
    def __init__(self):
        self.scanned_barcodes = set()

    def read_barcodes(self, frame):
        barcodes = pyzbar.decode(frame)
        barcode_set = set()
        for barcode in barcodes:
            x, y, w, h = barcode.rect
            barcode_info = barcode.data.decode('utf-8')
            if barcode_info not in barcode_set and barcode_info not in self.scanned_barcodes:
                barcode_set.add(barcode_info)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        self.scanned_barcodes.update(barcode_set)
        return frame, barcode_set

    def save_barcodes(self):
        with open("ScannedBarcodes.json", "a") as file:
            for barcode in self.scanned_barcodes:
                json.dump({"Barcode": barcode}, file)
                file.write("\n")
