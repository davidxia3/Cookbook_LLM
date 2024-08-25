import requests
import json
import psycopg2
import time
from bs4 import BeautifulSoup

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

BASE_URL = 'https://api.spoonacular.com/recipes'

def get_retrieved_recipe_ids():
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM recipes;")
        return set([row[0] for row in cursor.fetchall()])

def fetch_recipe():
    response = requests.get(f'{BASE_URL}/random', params={'apiKey': SPOONACULAR_API_KEY, 'number': 1})
    response.raise_for_status()
    recipe = response.json()['recipes'][0]

    print("X-API-Quota-Request:", response.headers.get('X-API-Quota-Request'))
    print("X-API-Quota-Used:", response.headers.get('X-API-Quota-Used'))
    print("X-API-Quota-Left:", response.headers.get('X-API-Quota-Left'))
    print(" ")

    return recipe

def process_and_insert_recipe(recipe):
    with conn.cursor() as cursor:
        summary = ""
        instructions = ""
        try:
            summary = BeautifulSoup(recipe.get('summary'), 'html.parser').get_text()
            instructions = BeautifulSoup(recipe.get('instructions'), 'html.parser').get_text()
        except:
            pass
        
        price_per_serving = recipe.get('pricePerServing')
        if price_per_serving is not None:
            price_per_serving = price_per_serving / 100
        
        recipe_data = {
            'id': recipe.get('id'),
            'name': recipe.get('title'),
            'prep_time': recipe.get('preparationMinutes'),
            'cook_time': recipe.get('cookingMinutes'),
            'vegetarian': recipe.get('vegetarian'),
            'vegan': recipe.get('vegan'),
            'gluten_free': recipe.get('glutenFree'),
            'dairy_free': recipe.get('dairyFree'),
            'very_healthy': recipe.get('veryHealthy'),
            'cheap': recipe.get('cheap'),
            'very_popular': recipe.get('veryPopular'),
            'sustainable': recipe.get('sustainable'),
            'price_per_serving': price_per_serving,
            'ready_in_minutes': recipe.get('readyInMinutes'),
            'summary': summary,
            'cuisines': recipe.get('cuisines'),
            'dish_types': recipe.get('dishTypes'),
            'diets': recipe.get('diets'),
            'occasions': recipe.get('occasions'),
            'instructions': instructions,
        }
        
        insert_recipe_query = """
        INSERT INTO recipes (
            id, name, prep_time, cook_time, vegetarian, vegan, gluten_free, 
            dairy_free, very_healthy, cheap, very_popular, sustainable, 
            price_per_serving, ready_in_minutes, summary, cuisines, dish_types, 
            diets, occasions, instructions
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (id) DO NOTHING;
        """
        
        cursor.execute(insert_recipe_query, (
            recipe_data['id'],
            recipe_data['name'],
            recipe_data['prep_time'],
            recipe_data['cook_time'],
            recipe_data['vegetarian'],
            recipe_data['vegan'],
            recipe_data['gluten_free'],
            recipe_data['dairy_free'],
            recipe_data['very_healthy'],
            recipe_data['cheap'],
            recipe_data['very_popular'],
            recipe_data['sustainable'],
            recipe_data['price_per_serving'],
            recipe_data['ready_in_minutes'],
            recipe_data['summary'],
            recipe_data['cuisines'],
            recipe_data['dish_types'],
            recipe_data['diets'],
            recipe_data['occasions'],
            recipe_data['instructions']
        ))

        for ingredient in recipe.get('extendedIngredients', []):
            if ingredient.get('id') == -1:
                continue
            
            insert_ingredient_query = """
            INSERT INTO ingredients (id, name, type, aisle, consistency)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """
            
            cursor.execute(insert_ingredient_query, (
                ingredient.get('id'),
                ingredient.get('name'),
                ingredient.get('type'),
                ingredient.get('aisle'),
                ingredient.get('consistency')
            ))
            
            insert_recipe_ingredient_query = """
            INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount, unit)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (recipe_id, ingredient_id) DO NOTHING;
            """
            
            cursor.execute(insert_recipe_ingredient_query, (
                recipe.get('id'),
                ingredient.get('id'),
                ingredient.get('amount'),
                ingredient.get('unit')
            ))
        
        conn.commit()


def main():
    already_fetched_ids = get_retrieved_recipe_ids()
    
    for _ in range(20): 
        recipe = fetch_recipe()
        
        if recipe['id'] not in already_fetched_ids:
            process_and_insert_recipe(recipe)
            already_fetched_ids.add(recipe['id'])
        
        time.sleep(1) 

if __name__ == "__main__":
    main()
    conn.close()
