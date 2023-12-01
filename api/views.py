from django.contrib.auth import get_user_model
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from recipes.models import Ingredient, Subscription, Favorite, Recipe
from purchases.shoppinglist import ShoppingList
from .serializers import (
    IngredientSerializer,
    SubscriptionSerializer,
    FavoriteSerializer,
    ShoppingListSerializer,
)


User = get_user_model()


class IngredientListAPIView(ListAPIView):
    """
    Allows retrieval of a list of all ingredients.
    Supports filtering ingredients by title using 'query' parameter.
    """

    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        query = self.request.query_params.get("query", None)

        if query is not None:
            queryset = queryset.filter(title__icontains=query)

        return queryset


class SubscriptionCreateAPIView(CreateAPIView):
    """
    Allows users to subscribe to authors.
    """
    serializer_class = SubscriptionSerializer


class SubscriptionDeleteAPIView(DestroyAPIView):
    """
    Allows users to unsubscribe from authors.
    """

    serializer_class = SubscriptionSerializer
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        Subscription.objects.filter(
            user=self.request.user, author=self.get_object()
        ).delete()
        return Response(data={"success": True})


class FavoriteCreateAPIView(CreateAPIView):
    """
    Allows users to add recipes to their favorites.
    """

    serializer_class = FavoriteSerializer


class FavoriteDeleteAPIView(DestroyAPIView):
    """
    Allows users to remove recipes from their favorites.
    """

    serializer_class = FavoriteSerializer
    queryset = Recipe.objects.all()

    def destroy(self, request, *args, **kwargs):
        Favorite.objects.filter(
            user=self.request.user, recipe=self.get_object()
        ).delete()
        return Response(data={"success": True})


class ShoppingListCreateAPIView(CreateAPIView):
    """
    Allows users to add recipes to their shopping lists.
    """

    serializer_class = ShoppingListSerializer
    queryset = Recipe.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request=request)
        return Response(data={"success": True})


class ShoppingListDestroyAPIView(DestroyAPIView):
    """
    Allows users to remove recipes from their shopping lists.
    """

    serializer_class = ShoppingListSerializer
    queryset = Recipe.objects.all()
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        recipe = self.get_object()
        shoppinglist = ShoppingList(request)
        shoppinglist.remove(recipe.id)
        return Response(data={"success": True})
