 import requests
from bing_image_urls import bing_image_urls
from pprint import pprint
class BarcodeInput:
    @staticmethod
    def scan(barcode):
        # TODO: get the image link instead of the website link...
        imageUrl = bing_image_urls(barcode, limit=1)[0] 
        # imageUrl = None
        url = f"https://world.openfoodfacts.org/api/v0/products/{barcode}.json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # print(data)
            product_data = data.get("product")
            if product_data is not None:
                return {
                    "name": product_data.get("product_name", None),
                    "brand": product_data.get("brands", None),
                    "quantity": product_data.get("quantity", None),
                    "energy_100g": product_data.get("nutriments", {}).get("energy-kcal_100g", None),
                    "energy_unit": product_data.get("nutriments", {}).get("energy-kcal_unit", None),
                    "nutriscore": product_data.get("nutriscore_grade", None),
                    "bingImage_url": imageUrl,
                    "image_url": product_data.get("image_url", None),
                }
            else:
                print("No product data found for barcode:", barcode)
                return None
        else:
            print("Error retrieving product data for barcode:", barcode)
            return None

# print(BarcodeInput.scan(3017620422003))
