# YAML Like Models
YAMLLM is a library for communicating structured data with LLMs. YAMLLM handles the workflow of:

- Requesting a response in a given structure
- Parsing the response
- Validating the result matches the given structure

**YAMLLM improves the workflow by:**
- Ultra-concise syntax
- Automatically skipping any preface or comments
- More robus
- Same schema can be used for prompting and validation
- Build validations and corrections directly into the schema
- 10x faster than PyYAML for parsing simple YAML
- Fewer tokens than JSON

## Example Usage
### Schemas
Schemas are defined using python dicts and the atr class:

```
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
```
An atr by default requires a type and description. Optionally, we can pass a fixer function to correct common errors. We can pass a validation function to run additional checks on a value.

Fixes are passed before casting to the defined type, so we pass through unaffected values
```
# Fixer function to cast fractions into floats
def convert_fractions(amount_string):
  if "/" in amount_string:
    numerator, denominator = amount_string.split("/")
    try:
      amount_string = float(numerator) / float(denominator)
    except:
      return None

  return amount_string
```

### String Representations
The function print_schema() converts a schema to a string for use in prompts. E.g:
```
metadata:
  name: # str Recipe Name
  description: # str Short 2-3 sentence description of the recipe
  servings: # int Number of servings
ingredients:
  - name: # str Ingredient Name
    unit: # str Unit of measurement, grams preferred
    amount: # float Amount of ingredient in given unit
instructions:
  - description: # str Step description
    duration: # int Duration in minutes
    appliance: # str Appliance used to prepare the step
```

### Validation
String responses from the LLM can be parsed into a python object, cast to the desired type, and validated against the schema. The object will be None if the validation fails.
```
recipe_object = parse_and_validate(response, recipe_schema)
```