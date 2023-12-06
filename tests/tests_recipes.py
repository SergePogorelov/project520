from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from recipes.models import (
    Ingredient,
    IngredientValue,
    Recipe,
    Favorite,
    Subscription
)
from recipes.utils import get_ingredients, create_ingridients


User = get_user_model()


class TestRecipes(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.author = User.objects.create(username='author')
        self.recipe_data = dict(
            author=self.author,
            name='Test Recipe',
            breakfast=True, lunch=False, dinner=True,
            cooking_time=10
        )
        self.recipe = Recipe.objects.create(**self.recipe_data)
        self.client = Client()
        self.client.force_login(self.user)

        self.favorite = Favorite.objects.create(user=self.user, recipe=self.recipe)
        self.subscription = Subscription.objects.create(user=self.user, author=self.author)

        self.ingredient_1 = Ingredient.objects.create(title="Ingredient 1", dimension="grams")
        self.ingredient_2 = Ingredient.objects.create(title="Ingredient 2", dimension="liters")
        self.ingredient_data = {
            "nameIngredient_1": "Ingredient 1",
            "valueIngredient_1": 100,
            "nameIngredient_2": "Ingredient 2",
            "valueIngredient_2": 2,
        }

    def tearDown(self):
        self.recipe = None
        self.ingredient_1 = None
        self.ingredient_2 = None
        self.user = None

    def test_get_ingredients_empty(self):
        """Checks get_ingredients for an empty recipe."""
        ingredients = get_ingredients(self.recipe)
        self.assertEqual(len(ingredients), 0)

    def test_get_ingredients_with_values(self):
        """Checks get_ingredients for a recipe with ingredients."""

        ingredients = get_ingredients(self.recipe)
        self.assertEqual(len(ingredients), 0)

        IngredientValue.objects.create(ingredient=self.ingredient_1, recipe=self.recipe, value=100)
        IngredientValue.objects.create(ingredient=self.ingredient_2, recipe=self.recipe, value=2)

        ingredients = get_ingredients(self.recipe)
        self.assertEqual(len(ingredients), 2)

    def test_create_ingredients(self):
        """Checks create_ingredients for a recipe."""
        self.assertEqual(self.recipe.ingredients.count(), 0)
        self.assertEqual(IngredientValue.objects.count(), 0)

        create_ingridients(self.recipe, self.ingredient_data)

        self.assertEqual(self.recipe.ingredients.count(), 2)
        self.assertEqual(IngredientValue.objects.count(), 2)

    def test_create_ingredients_update(self):
        """Checks create_ingredients to update existing ingredients."""
        # Adding initial ingredients
        create_ingridients(self.recipe, self.ingredient_data)
        self.assertEqual(self.recipe.ingredients.count(), 2)
        self.assertEqual(IngredientValue.objects.get(ingredient=self.ingredient_1).value, 100)
        self.assertEqual(IngredientValue.objects.get(ingredient=self.ingredient_2).value, 2)

        updated_data = {
            "nameIngredient_1": "Ingredient 1",
            "valueIngredient_1": 200,
            "nameIngredient_2": "Ingredient 2",
            "valueIngredient_2": 3,
        }
        # Updating existing ingredients
        create_ingridients(self.recipe, updated_data)
        # Check if values got updated
        self.assertEqual(IngredientValue.objects.get(ingredient=self.ingredient_1).value, 200)
        self.assertEqual(IngredientValue.objects.get(ingredient=self.ingredient_2).value, 3)

    # Views

    def test_recipe_detail_view(self):
        """Test Recipe Detail View"""
        path = reverse('recipe_detail', kwargs={'username': self.recipe.author.username, 'slug': self.recipe.slug})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_recipe_create_view(self):
        """Test Recipe Create View"""
        path = reverse('recipe_create')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_recipe_non_author_update_view(self):
        """Test Recipe Non Author Update View"""
        path = reverse('recipe_edit', kwargs={'username': self.recipe.author.username, 'slug': self.recipe.slug})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)

    def test_recipe_author_update_view(self):
        """Test Recipe Author Update View"""
        self.client.force_login(self.author)
        path = reverse('recipe_edit', kwargs={'username': self.recipe.author.username, 'slug': self.recipe.slug})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_view(self):
        """Test Recipe List View"""
        path = reverse('recipe_list')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_author_recipe_list_view(self):
        """Test Author Recipe List View"""
        path = reverse('author_recipe_list', kwargs={'username': self.user.username})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_favorite_recipe_list_view(self):
        """Test Favorite Recipe List View"""
        path = reverse('favorite_list', kwargs={'username': self.user.username})
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
