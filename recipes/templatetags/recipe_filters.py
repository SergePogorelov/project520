from django import template

from recipes.models import Favorite


register = template.Library()


@register.filter
def is_favorite(recipe_id, user_id):
    return Favorite.objects.filter(
        user_id=user_id, recipe_id=recipe_id
    ).exists()
