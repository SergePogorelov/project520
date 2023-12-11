# Foodrgram

This is an online service where users can publish recipes, subscribe to other users' publications, add favorite recipes to their "Favorites" list, and download a consolidated shopping list before going to the store, containing the ingredients needed to prepare one or more selected dishes.

## Project Description and Functionality

### Home Page

The main page displays a list of recipes sorted by publication date (from newest to oldest).

### Recipe Page

On this page, you can find the complete recipe description, the option to add the recipe to your favorites and shopping list, and the ability to subscribe to the recipe's author.

### User Page

This page displays the user's name, all recipes published by the user, and the option to subscribe to the user.

### Author Subscriptions

Subscribing to publications is available only to authorized users. The subscriptions page is accessible only to the account owner.

### User Behavior Scenario:

- A user can visit another user's page or a recipe page and subscribe to the author's publications by clicking the "Subscribe" button.
- Users can go to the "My Subscriptions" page to view the list of recipes published by authors they have subscribed to, sorted by publication date (from newest to oldest).
- If necessary, users can unsubscribe from an author by visiting the author's page or the author's recipe page and clicking "Unsubscribe from Author."

### Favorites List

Working with the favorites list is available only to **authorized users**. The favorites list can be viewed only by its owner.

**User Behavior Scenario:**

- Users can mark one or several recipes as favorites by clicking the "Add to Favorites" button.
- Users can visit the "Favorites List" page to view their personalized list of favorite recipes.
- If necessary, users can remove a recipe from their favorites.

### Shopping List

Working with the shopping list is available to both **authorized and unauthorized** users. However, only the owner can view the shopping list.

**User Behavior Scenario:**

- Users can mark one or several recipes as shopping list items by clicking the "Add to Shopping" button.
- Users can visit the "Shopping List" page, where all added recipes are available. Users can click the "Download" button to get a file with a consolidated list and quantity of required ingredients for all recipes saved in the "Shopping List."
- If necessary, users can delete a recipe from the shopping list.

The shopping list is downloaded in PDF format. When downloading the shopping list, the ingredients are summed up. For example, if two recipes require sugar (5g in one recipe and 10g in another), the list will have one item: "Sugar - 15g."

### Tag Filtering
Clicking on a tag name displays a list of recipes marked with that tag. Filtering can be done based on multiple tags in an "OR" combination: if multiple tags are selected, the page will display recipes marked with at least one of those tags. When filtering on the user's page, only the selected user's recipes are filtered. When filtering on the favorites page, only the favorite recipes are filtered.

### Registration and Authentication
The project includes a user registration and authentication system. Mandatory fields for users include:

- Username
- Password
- Email

### What Unauthenticated Users Can Do

Unauthenticated users can:

- Create an account.
- View recipes on the main page.
- View individual recipe pages.
- View user pages.
- Filter recipes by tags.
- Work with a personalized shopping list: add/remove any recipes and download a file with the quantity of required ingredients for recipes in the shopping list.

### What Authenticated Users Can Do

Authenticated users can:

- Log in with their username and password.
- Log out.
- Reset their password.
- Change their password.
- Create/edit/delete their own recipes.
- View recipes on the main page.
- View user pages.
- View individual recipe pages.
- Filter recipes by tags.
- Work with a personalized favorites list: add/remove other users' recipes and view their own favorite recipes page.
- Work with a personalized shopping list: add/remove any recipes and download a file with the quantity of required ingredients for recipes in the shopping list.
- Subscribe to recipe authors' publications, unsubscribe, and view their own subscriptions page.


## Installation on a Local Computer
These instructions will help you create a copy of the project and run it on your local computer for development and testing purposes.

### Running the Project (Linux Example)

Before getting started, if you're not using `Python 3`, you'll need to install the `virtualenv` tool using `pip install virtualenv`. If you're using `Python 3`, you should already have the [venv](https://docs.python.org/3/library/venv.html) module installed as part of the standard library.

- Create a project folder named "foodgram" on your computer: `mkdir foodgram` and navigate to it: `cd foodgram`.
- Clone this repository into the current folder: `git clone https://github.com/SergePogorelov/foodgram .`
- Create a virtual environment: `python3 -m venv venv`.
- Activate the virtual environment: `source venv/bin/activate`.
- Create a file named `.env` and add the environment variables to it:

```
SECRET_KEY = # Django secret key
DEBUG=1
```
- Install the dependencies: `pip install -r requirements.txt`.
- Apply migrations: `python manage.py migrate`.
- Create a Django superuser: `python manage.py createsuperuser --username admin --email 'admin@example.com'`.
- Start the Django development server: `python manage.py runserver`.

## Running Tests

To execute the tests, use the following command:

```bash
python3 manage.py test tests
```

#### Measuring Coverage

To assess test coverage, run the tests with coverage:

```bash
coverage run manage.py test tests
```

To view the coverage report in the terminal, execute:

```bash
coverage report
```

To generate an HTML report for a more detailed view:
```bash
coverage html
```

The HTML report can be accessed at `htmlcov/index.html`.


## Technologies Used in Development
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Pillow](https://pypi.org/project/Pillow/)
- [Sorl-thumbnail](https://pypi.org/project/sorl-thumbnail/)
- [WeasyPrint](https://weasyprint.org/)
- [PostgreSQL](https://www.postgresql.org/)
