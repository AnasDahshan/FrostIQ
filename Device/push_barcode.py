from firebase_admin import firestore

class PushBarcode:
    def __init__(self, db):
        self.db = db

    def push_barcode_firebase(self, barcode):
        doc_ref = self.db.collection("scanned_barcodes").document()
        doc_ref.set({"barcode_number": barcode})
        print(f"Barcode stored in Firestore: {barcode}")
        print(f"Barcode document ID: {doc_ref.id}")
