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
import random
from Bard import Chatbot
import json


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

    # Prompt Bard with the updated question
    response = chatbot.ask(
        f"Prompted suggest me one unique recipe for breakfast, lunch, and dinner in detail in JSON format exactly like this format. Please make sure all recipes are in the same dictionary. Make sure the instructions are formatted this way: \"\"\" Insert String here \"\"\". Please! " + recipe_string + f" if the following items are available: {prompt_variation_str}, give a new one")

    response = response['content']
    print("Response:", response)  # Add this line to print the content of the response
    response = extract_chars_inside_braces(response)

    response = Converter(response)
    response_json = json.loads(response)

    # Delete old recipe documents in the 'recipes2' collection
    old_recipes = db.collection('recipes2').get()
    for old_recipe in old_recipes:
        db.collection('recipes2').document(old_recipe.id).delete()
        print(f"Deleted old recipe: {old_recipe.id}")

    # Store the response in Firestore
    for recipe_type in response_json:
        recipe_name = response_json[recipe_type]["name"]
        image_url = search_image(recipe_name)  # Call your image search function with the recipe name
        response_json[recipe_type]["image_url"] = image_url

    db.collection('recipes2').document().set(response_json)

cred = credentials.Certificate('/Users/onyx/Desktop/frost-iq-firebase-adminsdk-ooc0g-e7756d0f91.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

call_bard(db)
