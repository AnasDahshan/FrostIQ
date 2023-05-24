import datetime
import io
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import requests
from google.cloud import vision
from google.cloud.firestore_v1 import ArrayRemove
from googleapiclient.discovery import build
import re
import sys
import datetime
from Bard import Chatbot
import json
import random


# Initialize Firebase
cred = credentials.Certificate('/Users/onyx/Desktop/frost-iq-firebase-adminsdk-ooc0g-e7756d0f91.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
databaseToAddTo = "products_info"

# Setting up authentication for Vision API
vision_client = vision.ImageAnnotatorClient.from_service_account_file('/Users/onyx/Desktop/FrostIQ/ServerSide/pure-pact-324017-f60c5727bd0d.json')

# Setting up authentication for Google Search API
api_key = "AIzaSyATjF5shqAiA-ljZuXFjjIS3Tr1h8VeeFY"
cse_id = "45ce52ad908034398"

# Creating a Google Search service object
service = build('customsearch', 'v1', developerKey=api_key)


# Function to search for an image using Google Search API
def search_image(query):
    excluded_keywords = ['barcode', 'code']  # Keywords to exclude barcode images
    excluded_websites = ['https://upcfoodsearch.com/images/ean-13/0021000053674.png']  # Website to exclude
    query = f'{query} -{" -".join(excluded_keywords)}'  # Add negative keywords to exclude barcode images
    res = service.cse().list(q=query, cx=cse_id, searchType='image').execute()
    if 'items' in res:
        filtered_items = [item for item in res['items'] if not any(keyword in item['link'] or keyword in item.get('title', '') for keyword in excluded_keywords) and item['link'] not in excluded_websites]
        if filtered_items:
            return filtered_items[0]['link']
    return None


# Function to detect objects in an image using Google Vision API
def detect_objects(image_content):
    image = vision.Image(content=image_content)

    # Perform object detection
    response = vision_client.object_localization(image=image)
    objects = response.localized_object_annotations

    # Extract object names
    object_names = [obj.name for obj in objects]

    return object_names


# Function to perform label detection using Google Vision API
def detect_labels(image_content):
    image = vision.Image(content=image_content)

    # Perform label detection
    response = vision_client.label_detection(image=image)
    labels = response.label_annotations

    # Extract label descriptions
    label_descriptions = [label.description for label in labels]

    return label_descriptions


# Fetch scanned images from Firestore collection and update the products info database
def scannedImageAll():
    # Fetch scanned images from Firestore collection
    images_ref = db.collection('scanned_images')
    docs = images_ref.get()

    for doc in docs:
        image_data = doc.to_dict()  # Get the dictionary representation of the document
        image_url = image_data.get('image_url')

        # Fetch image content from URL
        image_response = requests.get(image_url)
        image_content = image_response.content

        # Perform object detection on the image
        detected_objects = detect_objects(image_content)

        # Check if any of the detected objects already exist in products_info collection
        for detected_object in detected_objects:
            existing_product = db.collection(databaseToAddTo).where('Name', '==', detected_object).limit(1).stream()
            if any(existing_product):
                print(f"Detected object '{detected_object}' already exists in 'products_info' collection. Skipping.")
                continue

            # Search for an image using the detected object name
            image_url = search_image(detected_object)
            if image_url is None:
                print(f"Failed to fetch image for detected object '{detected_object}'.")
                continue

            # Perform label detection on the image
            labels = detect_labels(image_content)

            # Check if the detected object matches any of the labels
            if detected_object.lower() in [label.lower() for label in labels]:
                # Add detected object details to Firestore collection
                timestamp = datetime.datetime.now()
                object_data = {
                    'Barcode': None,
                    'Name': detected_object,
                    'Image': image_url,
                    'Description': None,
                    'Calories': None,
                    'Timestamp': timestamp
                }
                db.collection(databaseToAddTo).add(object_data)

        print(f"Detected objects: {detected_objects}")


# --- Recipes Codes: 

def Converter(string):
    # Replace newlines within triple quotes
    string = string.replace(',]', ']')
    string = string.replace('}{', '}}{')
    pattern_quotes = r'"""([\s\S]*?)"""'
    repl_func_quotes = lambda match: '["' + '", "'.join(line.strip() for line in match.group(1).splitlines() if line.strip()) + '"]'
    string = re.sub(pattern_quotes, repl_func_quotes, string)
    
    # Replace `}}{` with `},"lunch_recipe":{` the first time
    string = string.replace('}}{', '},"lunch_recipe":{', 1)
    # Replace `}}{` with `},"dinner_recipe":{` the second time
    string = string.replace('}}{', '},"dinner_recipe":{', 1)
    
    return string


def extract_chars_inside_braces(text):
    inside_braces = False
    result = ""
    for char in text:
        if char == '{':
            inside_braces = True
            result += char
        elif char == '}':
            inside_braces = False
            result += char
        elif inside_braces:
            result += char
    return result


def call_bard(db):
    token = "WwiUjmcCuCJt7VCwGwHG7cZSUpmZFRI2IKPBfcg3QsR6TNEZoNIUbN1olea-dKMvPL9T8w."
    # Initialize Google Bard API
    chatbot = Chatbot(token)

    # Retrieve food items from Firestore
    collection_ref = db.collection("products_info")
    food_items = [doc.get("Name") for doc in collection_ref.stream()]
    print(food_items)

    # Join the food items into a single string
    food_items_str = " ".join(food_items)

    recipe_dict = {
        "breakfast_recipe": {
            "name": "",
            "ingredients": [],
            "instructions": """
                Instruction goes here
            """,
            "type": "breakfast",
            "image_url": ""
        },
        "lunch_recipe": {
            "name": "",
            "ingredients": [],
            "instructions": """
                Instruction goes here
            """,
            "type": "lunch",
            "image_url": ""
        },
        "dinner_recipe": {
            "name": "",
            "ingredients": [],
            "instructions": """
                Instruction goes here
            """,
            "type": "dinner",
            "image_url": ""
        }
    }

    recipe_string = json.dumps(recipe_dict)

    # Randomly choose words from the list for variation
    num_variations = 3  # Adjust the number of variations as needed
    prompt_variations = random.sample(food_items, num_variations)
    prompt_variation_str = ", ".join(prompt_variations)
    print(prompt_variation_str)

    response = chatbot.ask(
        f"Prompted suggest me one unique recipe for breakfast, lunch, and dinner in detail in JSON format exactly like this format. Please make sure all recipes are in the same dictionary. Make sure the instructions are formatted this way: \"\"\" Insert String here \"\"\". Please! " + recipe_string + f" if the following items are available: {prompt_variation_str}")

    response = response['content']
    print(response)

    response = extract_chars_inside_braces(response)
    response = Converter(response)

    try:
        response_json = json.loads(response)
    except json.JSONDecodeError:
        # Error occurred while parsing response as JSON
        print("Error occurred while parsing response as JSON. Keeping the old recipe in Firebase.")
        return

    # Store the response in Firestore
    for recipe_type in response_json:
        recipe_name = response_json[recipe_type]["name"]
        image_url = search_image(recipe_name)  # Call your image search function with the recipe name
        response_json[recipe_type]["image_url"] = image_url

    # Delete the old recipe in Firebase and upload the new one
    try:
        old_recipe_query = db.collection('recipes1').limit(1)
        old_recipes = old_recipe_query.get()
        for old_recipe in old_recipes:
            old_recipe.reference.delete()
            print("Old recipe successfully deleted from Firebase.")

        db.collection('recipes1').document().set(response_json)
        print("New recipe successfully uploaded to Firebase.")
    except Exception as e:
        print("Error occurred while updating the recipe in Firebase:", str(e))

# End of Recipes Code. ----


# End of Recipes Code. ----


def main():
    # # Lists to store successful and failed items
    # successful_items = []
    # failed_items = []

    # # Fetch barcode from Firestore collection
    # barcodes_ref = db.collection('scanned_barcodes')
    # docs = barcodes_ref.get()

    # for doc in docs:
    #     barcode_data = doc.to_dict()  
    #     barcode = barcode_data.get('barcode_number')

    #     # Check if barcode already exists in products_info collection
    #     products_ref = db.collection(databaseToAddTo)
    #     existing_product = products_ref.where('Barcode', '==', barcode).limit(1).stream()
    #     if any(existing_product):
    #         print(f"Barcode {barcode} already exists in 'products_info' collection. Skipping.")
    #         continue

    #     # Search for an image using the barcode
    #     image_url = search_image(barcode)
    #     if image_url is None:
    #         failed_items.append(barcode)
    #         print(f"Failed to fetch image for barcode {barcode}.")
    #         continue

    #     # Fetch product details from Open Food Facts API
    #     api_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    #     response = requests.get(api_url)
    #     data = response.json()

    #     if data.get('status') == 1:
    #         product = data.get('product')

    #         # Extract relevant details from the API response
    #         name = product.get('product_name')
    #         description = product.get('generic_name')
    #         nutriments = product.get('nutriments', {})
    #         calories = None
    #         for key in nutriments:
    #             if 'energy-kcal' in key.lower() or 'energy_100g' in key.lower():
    #                 calories = nutriments[key]
    #                 break
    #         if calories is not None:
    #             calories = round(float(calories))  # Round the calories to the nearest whole number

    #         # Add product details to Firestore collection
    #         timestamp = datetime.datetime.now()
    #         product_data = {
    #             'Barcode': barcode,
    #             'Name': name,
    #             'Image': image_url,
    #             'Description': description,
    #             'Calories': calories,
    #             'Timestamp': timestamp
    #         }
    #         products_ref.document(barcode).set(product_data)
    #         successful_items.append(barcode)
    #         print(f"Barcode {barcode} details added to 'products_info' collection at {timestamp}.")
    #     else:
    #         failed_items.append(barcode)
    #         print(f"Failed to fetch details for barcode {barcode}.")

    # # Call the new function to detect and store fruit or vegetable names
    # scannedImageAll()

    # # Cleanup: Optional step to ensure graceful termination
    # firebase_admin.delete_app(firebase_admin.get_app())

    # # Print the lists of successful and failed items
    # print("Successfully added items:")
    # for barcode in successful_items:
    #     product_data = products_ref.document(barcode).get().to_dict()
    #     timestamp = product_data.get('Timestamp')
    #     print(f"Barcode {barcode} details added to 'products_info' collection at {timestamp}")

    # print("Failed to fetch items:")
    # for barcode in failed_items:
    #     print(f"Failed to fetch details for barcode {barcode}.")

    # Calling Bard in order to store new recipes in the database
    call_bard(db)


if __name__ == "__main__":
    main()
