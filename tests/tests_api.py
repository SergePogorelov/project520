from django.contrib.auth import get_user_model
from django.test import TestCase
from django.http import Http404
from django.urls import reverse
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.test import APIClient
from unittest.mock import Mock

from api.serializers import (
    IngredientSerializer,
    SubscriptionSerializer,
    FavoriteSerializer,
)
from recipes.models import Favorite, Recipe


User = get_user_model()


class TestSerializerApi(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.author = User.objects.create(username='author')

    def tearDown(self):
        self.user = None
        self.author = None

    def test_serializer(self):
        """Test if the IngredientSerializer validates valid data."""
        ingredient_data = {"title": "Sugar", "dimension": "cup"}
        serializer = IngredientSerializer(data=ingredient_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer(self):
        """Test if the IngredientSerializer raises an error with invalid data."""
        invalid_ingredient_data = {"title": "Flour"}
        serializer = IngredientSerializer(data=invalid_ingredient_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_method(self):
        """Test the SubscriptionSerializer's validation method for a valid subscription."""
        subscription_data = {"id": self.author.id}
        context = {'request': Mock(user=self.user)}
        serializer = SubscriptionSerializer(data=subscription_data, context=context)
        self.assertTrue(serializer.is_valid())

    def test_invalid_subscription(self):
        """Test if the SubscriptionSerializer rejects subscription to oneself."""
        subscription_data = {"id": self.user.id}
        context = {'request': Mock(user=self.user)}
        serializer = SubscriptionSerializer(data=subscription_data, context=context)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_same_user_subscription(self):
        """Test if the SubscriptionSerializer raises error for subscribing to the same user."""
        subscription_data = {"id": self.user.id}
        context = {'request': Mock(user=self.user)}
        serializer = SubscriptionSerializer(data=subscription_data, context=context)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class TestFavoriteSerializer(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.recipe = Recipe.objects.create(
            author=self.user,
            name='Test Recipe',
            breakfast=True, lunch=False, dinner=True,
            cooking_time=10
        )

    def tearDown(self):
        self.user = None
        self.recipe = None

    def test_validate_method(self):
        """Test the FavoriteSerializer's validation method for a valid favorite."""
        favorite_data = {"id": self.recipe.id}
        context = {'request': Mock(user=self.user)}
        serializer = FavoriteSerializer(data=favorite_data, context=context)
        self.assertTrue(serializer.is_valid())

    def test_invalid_favorite(self):
        """Test if the FavoriteSerializer raises Http404 for an invalid favorite."""
        favorite_data = {"id": 9999}  # Non-existing recipe ID
        context = {'request': Mock(user=self.user)}
        serializer = FavoriteSerializer(data=favorite_data, context=context)
        with self.assertRaises(Http404):
            serializer.is_valid(raise_exception=True)

    def test_duplicate_favorite(self):
        """Test if the FavoriteSerializer rejects duplicate favorites."""
        favorite_data = {"id": self.recipe.id}
        Favorite.objects.create(user=self.user, recipe=self.recipe)
        context = {'request': Mock(user=self.user)}
        serializer = FavoriteSerializer(data=favorite_data, context=context)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class TestAPIView(TestCase):
    """Tests the IngredientListAPIView functionality."""

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.author = User.objects.create(username='author')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.recipe = Recipe.objects.create(
            author=self.user,
            name='Test Recipe',
            breakfast=True, lunch=False, dinner=True,
            cooking_time=10
        )

    def tearDown(self):
        self.user = None
        self.author = None
        self.client = None
        self.recipe = None

    def test_get_all_ingredients(self):
        """Ensures that all ingredients can be retrieved."""
        response = self.client.get(reverse('ingredients_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_ingredients_by_title(self):
        """Validates the filtering of ingredients by title."""
        response = self.client.get(reverse('ingredients_list'), {'query': 'sugar'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscription_creation(self):
        """Validates the creation of a subscription."""
        response = self.client.post(reverse('create_subscriptions'), {'id': self.author.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_favorite_creation(self):
        """Validates the creation of a favorite."""
        response = self.client.post(reverse('create_favorites'), {'id': self.recipe.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_favorite_deletion(self):
        """Validates the deletion of a favorite."""
        response = self.client.delete(reverse('delete_favorites', kwargs={'pk': self.recipe.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shopping_list_creation(self):
        """Validates the creation of a shopping list."""
        response = self.client.post(reverse('create_purchases'), {'id': self.recipe.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shopping_list_deletion(self):
        """Validates the deletion of a shopping list."""
        self.client.post(reverse('create_purchases'), {'id': self.recipe.id})
        response = self.client.delete(reverse('delete_purchases', kwargs={'pk': self.recipe.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
