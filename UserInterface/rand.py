import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Set up credentials
cred = credentials.Certificate('/Users/onyx/Desktop/frost-iq-firebase-adminsdk-ooc0g-e7756d0f91.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore database
db = firestore.client()

# Collection name
collection_name = 'recipes2'

# Retrieve all documents from the collection
docs = db.collection(collection_name).stream()

for doc in docs:
    data = doc.to_dict()  # Convert document to dictionary

    # Define the meal types
    meal_types = ['breakfast_recipe', 'lunch_recipe', 'dinner_recipe']

    for meal_type in meal_types:
        meal_recipe = data.get(meal_type, {})
        image_url = meal_recipe.get('image_url', '')
        name = meal_recipe.get('name', '')
        recipe_type = meal_recipe.get('type', '')
        ingredients = meal_recipe.get('ingredients', [])
        instructions = meal_recipe.get('instructions', [])

        # Do something with the recipe data
        print(f'{meal_type.capitalize()} - Image URL:', image_url)
        print(f'{meal_type.capitalize()} - Name:', name)
        print(f'{meal_type.capitalize()} - Type:', recipe_type)
        print(f'{meal_type.capitalize()} - Ingredients:', ingredients)
        print(f'{meal_type.capitalize()} - Instructions:', instructions)