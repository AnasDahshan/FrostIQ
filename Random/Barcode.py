import requests
import pandas as pd
import random
import openpyxl
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

# Load the xlsx file into a DataFrame
df = pd.read_excel('randomBarcodes.xlsx')

# Get the number of rows in the DataFrame
num_rows = df.shape[0]

# Select 5 random row indices
random_indices = random.sample(range(num_rows), 5)

# Loop through the selected rows and print the barcode value in the first column
for i in random_indices:
    barcode = df.iloc[i, 0]
    print(BarcodeInput.scan(barcode))

 