from django import template

from recipes.models import Favorite


register = template.Library()


@register.filter
def is_favorite(recipe_id, user_id):
    """
    Custom template filter to check if a recipe is marked as a favorite by a specific user.

    :param recipe_id: ID of the recipe to check.
    :type recipe_id: int
    :param user_id: ID of the user to check for favorite status.
    :type user_id: int
    :return: Boolean indicating whether the recipe is a favorite of the user.
    :rtype: bool
    """
    return Favorite.objects.filter(
        user_id=user_id, recipe_id=recipe_id
    ).exists()
