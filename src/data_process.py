import json
def process_recipes(recipe):
    recipe_data = {
        "id": recipe.get("id"),
        "name": "This recipe is called " + recipe.get("name") + ".",
        "prep_time": (
            recipe.get("name") + " needs " + str(recipe.get("prep_time")) + " minutes of preparation."
            if recipe.get("prep_time") is not None
            else ""
        ),        
        "cook_time": (
            recipe.get("name") + " needs " + str(recipe.get("cook_time")) + " minutes to cook."
            if recipe.get("cook_time") is not None
            else ""
        ),
        "vegetarian": (
            recipe.get("name") + " is vegetarian."
            if recipe.get("vegetarian")
            else recipe.get("name") + " is not vegetarian."
        ),
        "vegan": (
            recipe.get("name") + " is vegan."
            if recipe.get("vegan")
            else recipe.get("name") + " is not vegan."
        ),
        "gluten_free": (
            recipe.get("name") + " is gluten free."
            if recipe.get("gluten_free")
            else recipe.get("name") + " is not gluten free."
        ),
        "dairy_free": (
            recipe.get("name") + " is dairy free."
            if recipe.get("dairy_free")
            else recipe.get("name") + " is not dairy free."
        ),
        "very_healthy": (
            recipe.get("name") + " is very_healthy."
            if recipe.get("very_healthy")
            else recipe.get("name") + " is not very healthy."
        ),
        "cheap": (
            recipe.get("name") + " is cheap."
            if recipe.get("cheap")
            else recipe.get("name") + " is not cheap."
        ),
        "very_popular": (
            recipe.get("name") + " is very popular."
            if recipe.get("very_popular")
            else recipe.get("name") + " is not very popular."
        ),
        "sustainable": (
            recipe.get("name") + " is sustainable."
            if recipe.get("sustainable")
            else recipe.get("name") + " is not sustainable."
        ),
        "price_per_serving": (
            "The price per serving of " + recipe.get("name") + " is " + recipe.get("price_per_serving") + "."
            if recipe.get("price_per_serving") is not None
            else ""
        ),
        "ready_in_minutes": (
            recipe.get("name") + " is ready in " + str(recipe.get("ready_in_minutes")) + " minutes."
            if recipe.get("ready_in_minutes") is not None
            else ""
        ),
        "summary": (
            recipe.get("summary")
            if recipe.get("summary") is not None
            else ""
        ),
        "price_per_serving": (
            "The price per serving of " + recipe.get("name") + " is $" + recipe.get("price_per_serving") + "."
            if recipe.get("price_per_serving") is not None
            else ""
        ),
       "cuisines": (
            ""
            if not recipe.get("cuisines")
            else f'{recipe.get("name")} is {recipe.get("cuisines")[0]} cuisine.'
            if len(recipe.get("cuisines")) == 1
            else f'{recipe.get("name")} is {", ".join(recipe.get("cuisines")[:-1])}, and {recipe.get("cuisines")[-1]} cuisine.'
            if len(recipe.get("cuisines")) == 2
            else f'{recipe.get("name")} is {", ".join(recipe.get("cuisines")[:-1])}, and {recipe.get("cuisines")[-1]} cuisine.'
        ),
        "dish_types": (
            ""
            if not recipe.get("dish_types")
            else f'{recipe.get("name")} is for {recipe.get("dish_types")[0]}.'
            if len(recipe.get("dish_types")) == 1
            else f'{recipe.get("name")} is for {", ".join(recipe.get("dish_types")[:-1])}, and {recipe.get("dish_types")[-1]}.'
            if len(recipe.get("dish_types")) == 2
            else f'{recipe.get("name")} is for {", ".join(recipe.get("dish_types")[:-1])}, and {recipe.get("dish_types")[-1]}.'
        ),
        "diets": (
            ""
            if not recipe.get("diets")
            else f'{recipe.get("name")} is {recipe.get("diets")[0]}.'
            if len(recipe.get("diets")) == 1
            else f'{recipe.get("name")} is {", ".join(recipe.get("diets")[:-1])}, and {recipe.get("diets")[-1]}.'
            if len(recipe.get("diets")) == 2
            else f'{recipe.get("name")} is {", ".join(recipe.get("diets")[:-1])}, and {recipe.get("diets")[-1]}.'
        ),
        "occasions": (
            ""
            if not recipe.get("occasions")
            else f'{recipe.get("name")} is popular for {recipe.get("occasions")[0]}.'
            if len(recipe.get("occasions")) == 1
            else f'{recipe.get("name")} is popular for {", ".join(recipe.get("occasions")[:-1])}, and {recipe.get("occasions")[-1]}.'
            if len(recipe.get("occasions")) == 2
            else f'{recipe.get("name")} is popular for {", ".join(recipe.get("occasions")[:-1])}, and {recipe.get("occasions")[-1]}.'
        ),
        "instructions": recipe.get("instructions", "")
    }
    return recipe_data

def process_ingredients(ingredient):
    ingredient_data = {
        "id": ingredient.get("id"),
        "name": "This ingredient is called " + ingredient.get("name") + ".",
        "type": (
            ingredient.get("name") + " is of type " + ingredient.get("type") + "."
            if ingredient.get("type") is not None
            else ""
        ),      
        "aisle": (
            ingredient.get("name") + " can be found in the " + ingredient.get("aisle").lower() + " aisle."
            if ingredient.get("aisle") is not None and not "," in ingredient.get("aisle")
            else (
                ingredient.get("name") + " can be found in the " + ingredient.get("aisle").lower() + " aisles."
                if ingredient.get("aisle") is not None
                else ""
            )
        ),
        "consistency": (
            ingredient.get("name") + " is a " + ingredient.get("consistency").lower() + "."
            if ingredient.get("consistency") is not None
            else ""
        )
    }
    return ingredient_data

def process_recipe_ingredients(recipe_ingredient):
    recipe_ingredient_data = {
        "recipe_id": recipe_ingredient.get("recipe_id"),
        "ingredient_id": recipe_ingredient.get("ingredient_id"),
        "unit_and_amount": " uses " + recipe_ingredient.get("amount") + " " + recipe_ingredient.get("unit") + " of "
        if recipe_ingredient.get("amount") !="" and recipe_ingredient.get("unit") !=""
        else ""
    }
    return recipe_ingredient_data

def json_to_jsonl(input_file, output_file, process_function):
    with open(input_file, "r") as json_file, open(output_file, "w") as jsonl_file:
        data = json.load(json_file)

        for item in data:
            processed_item = process_function(item) 
            jsonl_file.write(json.dumps(processed_item) + "\n")

if __name__ == "__main__":
    json_to_jsonl("data/json_data/recipes_data.json", "data/jsonl_data/recipes_data.jsonl", process_recipes)
    json_to_jsonl("data/json_data/ingredients_data.json", "data/jsonl_data/ingredients_data.jsonl", process_ingredients)
    json_to_jsonl("data/json_data/recipe_ingredients_data.json", "data/jsonl_data/recipe_ingredients_data.jsonl", process_recipe_ingredients)

