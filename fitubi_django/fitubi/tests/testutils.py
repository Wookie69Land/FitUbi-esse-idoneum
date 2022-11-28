from random import sample, randint, choice
from faker import Faker, Factory
from faker_food import FoodProvider

import random

from fitubi.models import User, FitUbiUser, Ingredient, Recipe, Plan
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


def create_fake_recipe():
    user = create_user()
    fake = Faker()
    fake.add_provider(FoodProvider)
    name = fake.dish()
    description = fake.dish_description()
    category = random.choice(RECIPE_CATEGORY)[0]
    type = str(RECIPE_CATEGORY[1][0])
    recipe = Recipe.objects.create(name=name, description=description,
                                   category=category, created_by=user,
                                   type=type)
    return recipe


def find_person_by_name(name):
    return User.objects.filter(username=name).first()


def count_users():
    return User.objects.all().count()


def count_fitubiusers():
    return FitUbiUser.objects.all().count()


def check_fitubiuser(user):
    return FitUbiUser.objects.filter(user=user).exists()
