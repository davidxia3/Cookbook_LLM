import json

def process(recipes_file, relational_file, ingredients_file, output_file):
    with open(recipes_file) as r, open(relational_file) as relational, open(ingredients_file) as i, open(output_file, 'w') as output:
        recipes = json.load(r)
        relationals = json.load(relational)
        ingredients = json.load(i)

        # Create a dictionary for quick ingredient lookup by ID
        ingredient_dict = {ingredient.get("id"): ingredient.get("name") for ingredient in ingredients}

        # Process each recipe
        for recipe in recipes:
            ingredient_ids = [rel.get("ingredient_id") for rel in relationals if rel.get("recipe_id") == recipe.get("id")]
            
            ingredient_names = [ingredient_dict.get(ingredient_id) for ingredient_id in ingredient_ids if ingredient_dict.get(ingredient_id)]

            if len(ingredient_names) == 0:
                completion_string = f"There are no ingredients in '{recipe.get('name')}'."
            elif len(ingredient_names) == 1:
                completion_string = f"{ingredient_names[0]} is in '{recipe.get('name')}'."
            elif len(ingredient_names) == 2:
                completion_string = f"{ingredient_names[0]} and {ingredient_names[1]} are in '{recipe.get('name')}'."
            else:
                completion_string = f"{', '.join(ingredient_names[:-1])}, and {ingredient_names[-1]} are in '{recipe.get('name')}'."

            recipe_data = {
                "prompt": f"What ingredients are in '{recipe.get('name')}'?",
                "completion": completion_string
            }
            output.write(json.dumps(recipe_data) + "\n")

        # Process each ingredient for aisle prompts
        for ingredient in ingredients:
            aisle = ingredient.get("aisle")
            if aisle:
                aisle_completion = f"{ingredient.get('name')} can be found in the {aisle.lower()} aisle."
            else:
                aisle_completion = f"The aisle information for {ingredient.get('name')} is not available."

            ingredient_data = {
                "prompt": f"What aisle is {ingredient.get('name')} in?",
                "completion": aisle_completion
            }
            output.write(json.dumps(ingredient_data) + "\n")


if __name__ == "__main__":
    process("data/json_data/recipes_data.json", "data/json_data/recipe_ingredients_data.json", "data/json_data/ingredients_data.json", "data/jsonl_data/prompts.jsonl")
