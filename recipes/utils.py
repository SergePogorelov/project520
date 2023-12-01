from .models import Ingredient, IngredientValue


def get_ingredients(recipe):
    """
    Retrieves ingredients for a given recipe.

    Given a recipe, this function fetches its associated ingredients and their values.
    It constructs a list of tuples containing ingredient title, value, and dimension.

    :param recipe: Recipe instance for which ingredients are to be retrieved.
    :type recipe: Recipe
    :return: List of tuples with ingredient details (title, value, dimension).
    :rtype: list
    """
    ingredients = []
    for ingredient in recipe.ingredients.all():
        value = ingredient.ingredient_values.get(recipe=recipe)
        ingredients.append((ingredient.title, value, ingredient.dimension))
    return ingredients


def create_ingridients(recipe, data):
    """
    Creates ingredients for a recipe based on provided data.

    This function is responsible for creating or updating ingredients and their values
    based on the data provided (usually from a form).

    :param recipe: Recipe instance for which ingredients are to be created/updated.
    :type recipe: Recipe
    :param data: Data containing ingredient details from a form.
    :type data: dict
    """
    for key, value in data.items():
        arg = key.split("_")
        if arg[0] == "nameIngredient":
            title = value
        if arg[0] == "valueIngredient":
            # Get or create the ingredient instance
            ingredient, _ = Ingredient.objects.get_or_create(
                title=title, defaults={"dimension": "p."}
            )
            # Update or create the ingredient value for the recipe
            IngredientValue.objects.update_or_create(
                ingredient=ingredient, recipe=recipe, defaults={"value": value}
            )
