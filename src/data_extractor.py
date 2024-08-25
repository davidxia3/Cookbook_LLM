import psycopg2
import json

with open('config.json') as config_file:
    config = json.load(config_file)
    DB_PASSWORD = config.get("master_password")
    SPOONACULAR_API_KEY = config.get('spoonacular_api_key')

conn = psycopg2.connect(
    dbname='cookbook_db',
    user='master',
    password=DB_PASSWORD,
    host='localhost'
)

def fetch_recipes():
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, prep_time, cook_time, vegetarian, vegan, gluten_free, dairy_free, very_healthy, cheap, very_popular, sustainable, price_per_serving, ready_in_minutes, summary, cuisines, dish_types, diets, occasions, instructions FROM recipes;")
        recipes = cursor.fetchall()
        
        data = []
        for recipe in recipes:
            data.append({
                'id': recipe[0],
                'name': recipe[1],
                'prep_time': recipe[2],
                'cook_time': recipe[3],
                'vegetarian': recipe[4],
                'vegan': recipe[5],
                'gluten_free': recipe[6],
                'dairy_free': recipe[7],
                'very_healthy': recipe[8],
                'cheap': recipe[9],
                'very_popular': recipe[10],
                'sustainable': recipe[11],
                'price_per_serving': str(recipe[12]),
                'ready_in_minutes': recipe[13],
                'summary': recipe[14],
                'cuisines': recipe[15],
                'dish_types': recipe[16],
                'diets': recipe[17],
                'occasions': recipe[18],
                'instructions': recipe[19]
            })
        
        return data

recipes = fetch_recipes()

with open('data/json_data/recipes_data.json', 'w') as json_file:
    json.dump(recipes, json_file, indent=4)


def fetch_ingredients():
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, type, aisle, consistency FROM ingredients;")
        ingredients = cursor.fetchall()
        
        data = []
        for ingredient in ingredients:
            data.append({
                'id': ingredient[0],
                'name': ingredient[1],
                'type': ingredient[2],
                'aisle': ingredient[3],
                'consistency': ingredient[4]
            })
        
        return data
    
ingredients = fetch_ingredients()

with open('data/json_data/ingredients_data.json', 'w') as json_file:
    json.dump(ingredients, json_file, indent=4)


def fetch_recipe_ingredients():
    with conn.cursor() as cursor:
        cursor.execute("SELECT recipe_id, ingredient_id, unit, amount FROM recipe_ingredients;")
        recipe_ingredients = cursor.fetchall()
        
        data = []
        for recipe_ingredient in recipe_ingredients:
            data.append({
                'recipe_id': recipe_ingredient[0],
                'ingredient_id': recipe_ingredient[1],
                'unit': recipe_ingredient[2],
                'amount': str(recipe_ingredient[3])
            })
        
        return data
    
recipe_ingredients = fetch_recipe_ingredients()

with open('data/json_data/recipe_ingredients_data.json', 'w') as json_file:
    json.dump(recipe_ingredients, json_file, indent=4)

conn.close()
