from random import sample, randint, choice
from faker import Faker, Factory
from faker_food import FoodProvider

import random

from fitubi.models import User, FitUbiUser, Ingredient, Recipe, RecipeIngredients, Plan, RecipePlan
from fitubi.choices import *


faker = Faker("en")


def random_user():
    users = User.objects.all()
    return choice(users)


def create_name():
    fake = Factory.create("en")
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = first_name + last_name + str(random.randint(1, 666))
    return username


def create_user():
    username = create_name()
    fake = Factory.create("en")
    email = fake.email()
    password = "fakefake"
    person = User.objects.create_user(username=username,
                                      email=email,
                                      password=password)
    return person


def create_fitubiuser():
    username = create_name()
    fake = Factory.create("en")
    email = fake.email()
    password = "fakefake"
    person = User.objects.create_user(username=username,
                                      email=email,
                                      password=password)
    person.fitubiuser.birth_date = fake.date()
    person.fitubiuser.food_preference = random.choice(DIET_TYPE)[0]
    person.fitubiuser.height = random.randint(150, 220)
    person.fitubiuser.weight = random.randint(40, 150)
    person.fitubiuser.sex = random.choice(SEX)[0]
    person.fitubiuser.activity = random.choice(ACTIVE_FACTOR)[0]

    return person


def create_fake_ingredient():
    fake = Faker()
    fake.add_provider(FoodProvider)
    name = fake.ingredient()
    while Ingredient.objects.filter(name=name).exists():
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
    return ingredient


def create_fake_recipe():
    user = create_user()
    fake = Faker()
    fake.add_provider(FoodProvider)
    name = fake.dish()
    while Recipe.objects.filter(name=name).exists():
        name = fake.dish()
    description = fake.dish_description()
    category = random.choice(RECIPE_CATEGORY)[0]
    type = str(RECIPE_CATEGORY[1][0])
    recipe = Recipe.objects.create(name=name, description=description,
                                   category=category, created_by=user,
                                   type=type)
    i = random.randint(2, 5)
    for _ in range(1, i):
        ingredient = create_fake_ingredient()
        amount = random.randint(1, 100)
        RecipeIngredients.objects.create(recipe=recipe, ingredient=ingredient, amount=amount)
    recipe.refresh_from_db()
    return recipe


def find_person_by_name(name):
    return User.objects.filter(username=name).first()


def count_users():
    return User.objects.all().count()


def count_fitubiusers():
    return FitUbiUser.objects.all().count()


def check_fitubiuser(user):
    return FitUbiUser.objects.filter(user=user).exists()


def create_fake_fridge():
    fake = Faker()
    fake.add_provider(FoodProvider)
    names = ['test fridge 1', 'test fridge 2']
    for name in names:
        unit = random.choice(UNIT)[0]
        carbs = random.randint(1, 10)
        fats = random.randint(1, 10)
        proteins = random.randint(1, 10)
        calories = random.randint(1, 10)
        category = random.choice(FOODCAT)[0]
        specials = fake.text()
        dangers = fake.text()
        Ingredient.objects.create(name=name, unit=unit, carbs=carbs,
                                               fats=fats, proteins=proteins,
                                               calories=calories, category=category,
                                               specials=specials, dangers=dangers)
    return Ingredient.objects.filter(name__icontains='test fridge')


def create_fake_fridge_recipe(ingredients):
    user = create_user()
    fake = Faker()
    fake.add_provider(FoodProvider)
    name = 'fridge recipe'
    description = fake.dish_description()
    category = random.choice(RECIPE_CATEGORY)[0]
    type = str(DIET_TYPE[0][0])
    recipe = Recipe.objects.create(name=name, description=description,
                                   category=category, created_by=user,
                                   type=type)
    for ingredient in ingredients:
        amount = random.randint(1, 100)
        RecipeIngredients.objects.create(recipe=recipe, ingredient=ingredient, amount=amount)
    ingredient = Ingredient.objects.all().first()
    amount = random.randint(1, 100)
    RecipeIngredients.objects.create(recipe=recipe, ingredient=ingredient, amount=amount)
    recipe.refresh_from_db()
    return recipe


def create_fake_fridge_one():
    fake = Faker()
    fake.add_provider(FoodProvider)
    name = 'test fridge 1'
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
    return ingredient


def create_fake_fridge_recipe_one(ingredient):
    user = create_user()
    fake = Faker()
    fake.add_provider(FoodProvider)
    name = 'fridge recipe'
    description = fake.dish_description()
    category = random.choice(RECIPE_CATEGORY)[0]
    type = str(DIET_TYPE[0][0])
    recipe = Recipe.objects.create(name=name, description=description,
                                   category=category, created_by=user,
                                   type=type)

    amount = random.randint(1, 100)
    RecipeIngredients.objects.create(recipe=recipe, ingredient=ingredient, amount=amount)
    ingredient_2 = Ingredient.objects.all().first()
    amount = random.randint(1, 100)
    RecipeIngredients.objects.create(recipe=recipe, ingredient=ingredient_2, amount=amount)
    recipe.refresh_from_db()
    return recipe


def create_fake_plan(user):
    fake = Factory.create("en")
    name = f'Plan for {fake.first_name()}'
    description = fake.text()
    created_by = user
    plan = Plan.objects.create(name=name, description=description, created_by=created_by)
    return plan

