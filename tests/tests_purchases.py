from django.test import TestCase, Client
from unittest.mock import patch, MagicMock

from purchases.shoppinglist import ShoppingList


class TestShoppingList(TestCase):

    def setUp(self):
        self.client = Client()
        self.request = self.client.get('/').wsgi_request
        self.shopping_list = ShoppingList(self.request)
        self.recipe_id = 1

    def tearDown(self):
        self.client = None
        self.request = None
        self.shopping_list = None

    def test_init(self):
        """Test initialization of ShoppingList object."""
        self.assertEqual(self.shopping_list.session, self.request.session)
        self.assertEqual(self.shopping_list.shoppinglist, [])

    def test_add(self):
        """Test adding a recipe to the shopping list."""
        self.assertEqual(self.shopping_list.shoppinglist, [])
        self.shopping_list.add(self.recipe_id)
        self.assertEqual(self.shopping_list.shoppinglist, [self.recipe_id])

    def test_remove(self):
        """Test removing a recipe from the shopping list."""
        self.shopping_list.add(self.recipe_id)
        self.shopping_list.remove(self.recipe_id)
        self.assertEqual(self.shopping_list.shoppinglist, [])

    def test_len(self):
        """Test getting the length of the shopping list."""
        self.assertEqual(len(self.shopping_list), 0)
        self.shopping_list.shoppinglist.append(self.recipe_id)
        self.assertEqual(len(self.shopping_list), 1)

    @patch('purchases.shoppinglist.Recipe.objects.filter')
    def test_iter(self, mock_filter):
        """Test iterating through the shopping list."""
        self.shopping_list.shoppinglist.append(self.recipe_id)
        mock_recipe = MagicMock()
        mock_filter.return_value = [mock_recipe]
        for recipe in self.shopping_list:
            self.assertEqual(recipe, mock_recipe)
        mock_filter.assert_called_once_with(id__in=[self.recipe_id])

    @patch('purchases.shoppinglist.Recipe.objects.filter')
    def test_get_objects(self, mock_filter):
        """Test retrieving Recipe objects from the shopping list."""
        self.shopping_list.shoppinglist.append(self.recipe_id)
        self.shopping_list.get_objects()
        mock_filter.assert_called_once_with(id__in=[self.recipe_id])

    def test_clear(self):
        """Test clearing the shopping list."""
        self.assertIn('shoppinglist', self.shopping_list.session)
        self.shopping_list.clear()
        self.assertNotIn('shoppinglist', self.shopping_list.session)

    @patch('purchases.shoppinglist.get_ingredients')
    @patch('purchases.shoppinglist.Recipe.objects.filter')
    def test_get_ingredients_for_pdf(self, mock_filter, mock_get_ingredients):
        """Test generating ingredients for PDF from the shopping list."""
        self.shopping_list.add(self.recipe_id)
        mock_recipe = MagicMock()
        mock_filter.return_value = [mock_recipe]
        class IngredientValue:
            value = 100
        mock_get_ingredients.return_value = [("Ingredient", IngredientValue(), "unit")]
        ingredients = self.shopping_list.get_ingridients_for_pdf()
        self.assertEqual(ingredients, [["Ingredient", 100, "unit", [mock_recipe.name]]])


class TestShoppingListViews(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        self.client = None

    def test_shoppinglist_detail_view(self):
        """Test the shopping list detail view."""
        response = self.client.get('/purchases/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'purchases/shopList.html')

    @patch('purchases.views.render_to_string')
    @patch('purchases.views.weasyprint')
    def test_download_shoppinglist_view(self, mock_weasyprint, mock_render_to_string):
        """Test the download shopping list view."""
        # Mocking shopping list data
        ingridients = [['example', 100, 'unit', ['recipe1']], ['example2', 200, 'unit', ['recipe2']]]
        mock_render_to_string.return_value = 'html content'
        mock_response = mock_weasyprint.HTML.return_value.write_pdf.return_value
        mock_response.content = b'pdf content'

        # Mock the ShoppingList instance
        with patch('purchases.views.ShoppingList') as mock_shoppinglist:
            mock_shoppinglist.return_value.get_ingridients_for_pdf.return_value = ingridients
            response = self.client.get('/purchases/pdf/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/pdf')
            self.assertEqual(response['Content-Disposition'], 'filename="shoppinglist.pdf"')

