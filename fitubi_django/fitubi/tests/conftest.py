import os
import sys

import pytest

from django.test import Client


from .testutils import *

sys.path.append(os.path.dirname(__file__))
faker = Faker("en")


@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def set_up():
    create_fitubiuser()
    for _ in range(10):
        create_fake_recipe()
