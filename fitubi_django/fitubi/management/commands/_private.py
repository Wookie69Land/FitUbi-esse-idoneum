import random

from faker import Factory, Faker

from fitubi.models import *


def create_name():
    fake = Factory.create("en")
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = first_name + last_name + str(random.randint(1, 666))
    return username, first_name, last_name


def create_user():
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


