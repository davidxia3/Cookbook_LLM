import requests
import json

# Load API key from config
with open('config.json') as config_file:
    config = json.load(config_file)
    SPOONACULAR_API_KEY = config.get('spoonacular_api_key')

BASE_URL = 'https://api.spoonacular.com/recipes'

def fetch_recipes():
    response = requests.get(f'{BASE_URL}/random', params={'apiKey': SPOONACULAR_API_KEY, 'number': 5})
    response.raise_for_status()

    # Print out the quota-related headers
    print("X-API-Quota-Request:", response.headers.get('X-API-Quota-Request'))
    print("X-API-Quota-Used:", response.headers.get('X-API-Quota-Used'))
    print("X-API-Quota-Left:", response.headers.get('X-API-Quota-Left'))

    return response.json()

# Example usage
recipes_data = fetch_recipes()
