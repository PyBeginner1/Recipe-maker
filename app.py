from flask import Flask, render_template, request
import logging
from constants import *
import requests 


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')
    

@app.route("/food", methods = ['POST'])
def food():
    if request.method == "POST":
        user_ingredient = request.form.get('Enter a Ingredient')
        user_food = request.form.get('Enter a Food')

        if user_ingredient and user_ingredient.strip():            
            url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={user_ingredient}&apiKey={API_KEY}"
            response = requests.get(url)
            data = response.json()
            return render_template('home.html', food_list = ', '.join([recipe['title'] for recipe in data]), message = 'You can prepare the following food: ')
        elif user_food and user_food.strip():
            food_recipe_url = f"https://api.spoonacular.com/recipes/complexSearch?query={user_food}&apiKey={API_KEY}"
            response = requests.get(food_recipe_url)
            data = response.json()
            recipe_id = data['results'][0]['id'] if data['results'] else 'Recipe not found, try another word!'
            if isinstance(recipe_id, int):
                recipe_info_url = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions?apiKey={API_KEY}"
                response = requests.get(recipe_info_url)
                recipe_data = response.json()
                steps = [step["step"] for step in recipe_data[0]["steps"]]
                print(steps) 
                return render_template('home.html', food_list = '\n'.join(steps), message = 'Steps to prepare: ')
            else:
                steps = recipe_id
                return render_template('home.html', food_list = steps, message = 'Sorry!')         
            

if __name__ == '__main__':
    app.run()
