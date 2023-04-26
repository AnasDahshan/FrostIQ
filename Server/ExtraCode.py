from barcode_input import BarcodeInput
from product_database import ProductDatabase


database = ProductDatabase("test2.db")
for i in range(3):
    barcode = input("Enter barcode: ")
    product_info = BarcodeInput.scan(barcode)
    if product_info is None:
        print("Invalid barcode, try again.")
        continue
    database.add_product(product_info, barcode)

all_products = database.get_all_products()
# for product in all_products:
#     print(f"{product['name']} ({product['barcode']})")


