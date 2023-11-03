from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from unidecode import unidecode


User = get_user_model()


class Tag:
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    TAGS = [BREAKFAST, LUNCH, DINNER]


class Ingredient(models.Model):
    title = models.CharField("Title", max_length=50)
    dimension = models.CharField("Dimension", max_length=50)

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Author",
    )
    name = models.CharField("Name", max_length=50, unique=True)
    slug = models.SlugField(unique=True, db_index=True)
    breakfast = models.BooleanField("Breakfast")
    lunch = models.BooleanField("Lunch")
    dinner = models.BooleanField("Dinner")
    ingredients = models.ManyToManyField(
        Ingredient, verbose_name="Ingredients", through="IngredientValue"
    )
    cooking_time = models.PositiveSmallIntegerField(
        "Cooking Time", help_text="in minuts"
    )
    description = models.TextField("Description")
    image = models.ImageField("Image", upload_to="recipes/")
    pub_date = models.DateTimeField(
        "Publication date", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "recipe_detail",
            kwargs={"username": self.author.username, "slug": self.slug},
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def clean(self):
        if not self.breakfast and not self.lunch and not self.dinner:
            raise ValidationError("You must select at least one tag.")

    def display_favorites(self):
        return ", ".join(
            self.favorites.all().values_list("user__username", flat=True)
        )

    display_favorites.short_description = "In favorites"


class IngredientValue(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name="ingredient_values",
        on_delete=models.CASCADE,
        verbose_name="Ingredient",
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="ingredient_values",
        on_delete=models.CASCADE,
        verbose_name="Recipe",
    )
    value = models.PositiveSmallIntegerField("Value")

    class Meta:
        verbose_name = "Quantity of ingredients"
        verbose_name_plural = "Quantity of ingredients"

    def __str__(self):
        return str(self.value)


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f"{self.user} subscribed to {self.author}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorites"
    )

    class Meta:
        verbose_name = "Favorites"
        verbose_name_plural = "Favorites"

    def __str__(self):
        return f"{self.recipe} in favorites {self.user}"
