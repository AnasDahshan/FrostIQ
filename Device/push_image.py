import os
import datetime
from firebase_admin import storage

class PushImage:
    def __init__(self, db):
        self.db = db

    def push_image_firebase(self, image_path):
        bucket_name = "frost-iq.appspot.com"  # Replace with your actual bucket name
        bucket = storage.bucket(bucket_name)
        image_file = os.path.basename(image_path)
        blob = bucket.blob("raw_fruits&vegetables/" + image_file)
        blob.upload_from_filename(image_path)

        # Get the download URL of the uploaded image
        download_url = blob.generate_signed_url(
            version="v4", expiration=datetime.timedelta(minutes=15), method="GET"
        )

        # Save the image URL in Firestore
        doc_ref = self.db.collection("scanned_images").document()
        doc_ref.set({
            "image_url": download_url,
            "image_file": image_file
        })
        print(f"Image uploaded to Firebase Storage: {image_file}")
        print(f"Image URL saved in Firestore: {doc_ref.id}")
