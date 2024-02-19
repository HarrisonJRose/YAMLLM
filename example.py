from yamllm import atr, parse_and_validate, print_schema
from time import sleep

# Example: Generating a recipe
# We will ask the LLM to generate a recipe using our schema
# The simulated response has some issues, like fractional quantities and name issues
# We will use fixer functions to correct these as we parse the string
# A basic formatte function is used to display the response

def main():
  # First step, we want to build the prompt for the LLM
  example_task = "Write a recipe for spaghetti bolognese using the following YAML syntax:"
  
  prompt = example_task + "\n" + print_schema(recipe_schema)

  print("SENDING PROMPT:\n\n"+prompt)
  

  # Send the prompt to the LLM
  print("\nWaiting on response from OpenAI")
  response = fake_GPT_call(prompt)
  sleep(1)

  print("\nRAW RESPONSE:\n" + response)
  
  # Parse the response and validate it against the schema.
  # Can be done in steps or all at once
  parsed_response = parse_and_validate(response, recipe_schema)

  print("\n\nPARSED AND CORRECTED RESPONSE:\n")

  # Print the response. Skip error checking because it's a manufactured example
  print_recipe(parsed_response)

# FIXER FUNCTIONS
# ===============

# Fixer function to cast fractions into floats
def convert_fractions(amount_string):
  if "/" in amount_string:
    numerator, denominator = amount_string.split("/")
    try:
      amount_string = float(numerator) / float(denominator)
    except:
      return None
  
  return amount_string

# Fixer function to remove unnecessary ingredient details
def clean_ingredient_name(ingredient_name):
  if ", " in ingredient_name:
    ingredient_name = ingredient_name.split(", ")[0]
  return ingredient_name

# Example Schema
# ==============

recipe_schema = \
{"metadata": {
  "name": atr(str, "Recipe Name"),
  "description": atr(str, "Short 2-3 sentence description of the recipe"),
  "servings": atr(int, "Number of servings")},
"ingredients": [
  {"name": atr(str, "Ingredient Name", fix_func=clean_ingredient_name),
   "unit": atr(str, "Unit of measurement, grams preferred"),
   "amount": atr(float, "Amount of ingredient in given unit", fix_func=convert_fractions)}],
"instructions": [
  {"description": atr(str, "Step description"),
   "duration": atr(int, "Duration in minutes"),
   "appliance": atr(str, "Appliance used to prepare the step")}]
}

# SIMULATED OUTPUT OF GPT-4
# ==========================

example_output_string = \
"""metadata:
  name: "Spaghetti Bolognese"
  description: "A classic Italian pasta dish with a rich and hearty meat sauce. Perfect for a comforting meal."
  servings: 4
ingredients:
  - name: "Spaghetti"
    unit: "grams"
    amount: 400.0
  - name: "Ground Beef"
    unit: "grams"
    amount: 500.0
  - name: "Olive Oil"
    unit: "tablespoons"
    amount: 2.0
  - name: "Onion, finely chopped"
    unit: "grams"
    amount: 100.0
  - name: "Carrots, finely chopped"
    unit: "grams"
    amount: 100.0
  - name: "Celery Stalks, finely chopped"
    unit: "stalks"
    amount: "1/2"
  - name: "Garlic Cloves, minced"
    unit: "cloves"
    amount: 2.0
  - name: "Canned Tomatoes"
    unit: "grams"
    amount: 400.0
  - name: "Tomato Paste"
    unit: "tablespoons"
    amount: 2.0
  - name: "Beef Stock"
    unit: "ml"
    amount: 200.0
  - name: "Red Wine"
    unit: "ml"
    amount: 100.0
  - name: "Bay Leaves"
    unit: "pieces"
    amount: 2.0
  - name: "Salt"
    unit: "to taste"
    amount: 
  - name: "Black Pepper"
    unit: "to taste"
    amount: 
instructions:
  - description: "Heat olive oil in a large pan over medium heat. Add onions, carrots, and celery. Cook until softened."
    duration: 10
    appliance: "Stove"
  - description: "Add minced garlic and ground beef. Cook until beef is browned."
    duration: 10
    appliance: "Stove"
  - description: "Pour in red wine, and cook for a few minutes to reduce slightly."
    duration: 5
    appliance: "Stove"
  - description: "Add canned tomatoes, tomato paste, beef stock, bay leaves, salt, and pepper. Bring to a simmer, then cover and cook on low heat for at least 1 hour, stirring occasionally."
    duration: 60
    appliance: "Stove"
  - description: "In a separate pot, bring water to a boil. Add spaghetti and cook according to package instructions until al dente. Drain."
    duration: 10
    appliance: "Stove"
  - description: "Serve the bolognese sauce over the cooked spaghetti."
    duration: 5
    appliance: "None"
"""

# UTILITY FUNCTIONS
# =================

#To make the example much simpler to run, we'll use a fake openAI call
def fake_GPT_call(prompt):
  return example_output_string

def print_recipe(recipe):
  # Print recipe metadata
  print(f"{recipe['metadata']['name']}\n{'=' * len(recipe['metadata']['name'])}")
  print(f"Description: {recipe['metadata']['description']}")
  print(f"Servings: {recipe['metadata']['servings']}\n")

  # Print ingredients
  print("Ingredients:")
  for ingredient in recipe['ingredients']:
      name = ingredient['name']
      amount = ingredient.get('amount', 'N/A')  # Handle ingredients without a specific amount
      unit = ingredient.get('unit', '')
      print(f"- {name}: {amount} {unit}".strip())
  print()

  # Print instructions
  print("Instructions:")
  for i, instruction in enumerate(recipe['instructions'], start=1):
      description = instruction['description']
      duration = instruction.get('duration', 'N/A')  # Handle instructions without a specific duration
      appliance = instruction.get('appliance', 'N/A')  # Handle instructions without a specific appliance
      print(f"Step {i}: {description} (Duration: {duration} mins, Appliance: {appliance})")

main()



