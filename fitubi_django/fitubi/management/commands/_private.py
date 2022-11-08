import random

from faker import Factory, Faker
from faker_food import FoodProvider

from fitubi.models import *


def create_name():
    fake = Factory.create("en")
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = first_name + last_name + str(random.randint(1, 666))
    return username, first_name, last_name


def create_users():
    for person in range(0, 10):
        username, first_name, last_name = create_name()
        fake = Factory.create("en")
        email = fake.email()
        password = "fake"
        person = User.objects.create(username=username,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email,
                                    password=password)
        person.fitubiuser.birth_date = fake.date()
        person.fitubiuser.food_preference = random.choice(DIET_TYPE)[0]
        person.fitubiuser.height = random.randint(150, 220)
        person.fitubiuser.weight = random.randint(40, 150)
        person.fitubiuser.sex = random.choice(SEX)[0]


def create_ingredients():
    fake = Faker()
    fake.add_provider(FoodProvider)
    for i in range(1, 50):
        name = fake.ingredient()
        unit = random.choice(UNIT)[0]
        carbs = random.randint(1, 10)
        fats = random.randint(1, 10)
        proteins = random.randint(1, 10)
        calories = random.randint(1, 10)
        category = random.choice(FOODCAT)[0]
        specials = fake.text()
        dangers = fake.text()
        ingredient = Ingredient.objects.create(name=name, unit=unit, carbs=carbs,
                                               fats=fats, proteins=proteins,
                                               calories=calories, category=category,
                                               specials=specials, dangers=dangers)


def create_recipe():
    fake = Faker()
    fake.add_provider(FoodProvider)
    for i in range(1, 15):
        name = fake.dish()
        description = fake.dish_description()
        category = random.choice(RECIPE_CATEGORY)[0]
        recipe = Recipe.objects.create(name=name, description=description,
                                       category=category)


def create_ingredients_for_recipe():
    ingredients = list(Ingredient.objects.all())
    for recipe in Recipe.objects.all():
        for i in range(1, 5):
            ingredient = random.choice(ingredients)
            amount = random.randint(1, 500)
            RecipeIngredients.objects.create(recipe=recipe,
                                             ingredient=ingredient,
                                             amount=amount)


