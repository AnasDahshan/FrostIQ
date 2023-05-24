from flask import Flask, render_template, request, jsonify
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

# Initialize Firebase credentials
cred = credentials.Certificate('/Users/onyx/Desktop/frost-iq-firebase-adminsdk-ooc0g-e7756d0f91.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__, template_folder=os.path.expanduser('~/Desktop/FrostIQ/UserInterface'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sensor_data')
def sensor_data():
    try:
        temperature_collection_ref = db.collection('temperature')
        temperature_query = temperature_collection_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
        temperature_documents = temperature_query.get()

        temperature = None
        humidity = None

        for document in temperature_documents:
            data = document.to_dict()
            temperature = data.get('temperature')
            humidity = data.get('humidity')

        light_collection_ref = db.collection('light')
        light_query = light_collection_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
        light_documents = light_query.get()

        door_status = None

        for document in light_documents:
            data = document.to_dict()
            light_status = data.get('light_status')
            door_status = "Closed" if light_status == 1 else "Open"

        return jsonify(temperature=temperature, humidity=humidity, door_status=door_status)
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/view_items')
def view_items():
    collection_ref = db.collection('products_info')
    products = []
    for doc in collection_ref.order_by('Timestamp', direction=firestore.Query.DESCENDING).stream():
        product_data = doc.to_dict()
        product_data['id'] = doc.id  # Add the document ID to the product data
        products.append(product_data)
    return render_template('view_items.html', products=products)

@app.route('/delete_item', methods=['POST'])
def delete_item():
    item_id = request.form.get('item_id')  # Get the ID of the item to be deleted

    try:
        db.collection('products_info').document(item_id).delete()  # Delete the item from the database
        return 'success'  # Return a success message
    except Exception as e:
        return 'error'  # Return an error message

@app.route('/view_recipes')
def view_recipes():
    recipes = []

    # Retrieve all documents from the collection
    docs = db.collection('recipes1').stream()

    for doc in docs:
        data = doc.to_dict()

        # Define the meal types
        meal_types = ['breakfast_recipe', 'lunch_recipe', 'dinner_recipe']

        for meal_type in meal_types:
            meal_recipe = data.get(meal_type, {})
            recipe_data = {
                'type': meal_type.split('_')[0],
                'image_url': meal_recipe.get('image_url', ''),
                'name': meal_recipe.get('name', ''),
                'ingredients': meal_recipe.get('ingredients', []),
                'instructions': meal_recipe.get('instructions', [])
            }
            recipes.append(recipe_data)


    return render_template('view_recipes.html', recipes=recipes)
if __name__ == '__main__':
    app.run(port=7100)
