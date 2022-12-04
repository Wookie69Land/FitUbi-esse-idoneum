import pytest
from bs4 import BeautifulSoup

from django.shortcuts import reverse

from .testutils import *
from fitubi.choices import DIET_TYPE
from fitubi.forms import FridgeForm
from fitubi.models import UserActivatedPlan, UserPlans


@pytest.mark.django_db
def test_user_connection():
    users_count = count_users()
    fitubiusers_count = count_fitubiusers()
    user = create_user()
    assert count_users() == users_count + 1
    assert count_fitubiusers() == fitubiusers_count + 1
    assert FitUbiUser.objects.filter(user=user).exists() is True


@pytest.mark.django_db
def test_update_multiselectfield():
    recipe = create_fake_recipe()
    length1 = len(recipe.type)
    recipe.type = [str(DIET_TYPE[1][0]), str(DIET_TYPE[2][0])]
    recipe.save()
    length2 = len(recipe.type)
    recipe.type = [str(DIET_TYPE[1][0]), str(DIET_TYPE[2][0]), str(DIET_TYPE[3][0])]
    recipe.save()
    length3 = len(recipe.type)
    recipe.type = [str(DIET_TYPE[1][0]), str(DIET_TYPE[2][0]), str(DIET_TYPE[3][0]), str(DIET_TYPE[4][0])]
    recipe.save()
    length4 = len(recipe.type)
    recipe.type = [str(DIET_TYPE[1][0]), str(DIET_TYPE[3][0]), str(DIET_TYPE[4][0])]
    recipe.save()
    length5 = len(recipe.type)
    types = recipe.type
    recipe.refresh_from_db()
    length6 = len(recipe.type)
    assert length1 == 1
    assert length2 == length1 + 1
    assert length3 == length2 + 1
    assert length4 == length3 + 1
    assert length5 == length4 - 1
    assert types == ['2', '4', '5']
    assert length6 == 3

@pytest.mark.django_db
def test_fridge_view(client, set_up):
    user = User.objects.all().first()
    client.login(username=user.username, password='fakefake')
    url = reverse('fridge')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_fridge(client, set_up):
    user = User.objects.all().first()
    client.login(username=user.username, password='fakefake')
    url_reverse = reverse('fridge')
    ingredients = create_fake_fridge()
    recipe = create_fake_fridge_recipe(ingredients)
    data = {
        'ingredients': [ingredient.id for ingredient in ingredients],
        'category': recipe.category,
        'type': [str(DIET_TYPE[0][0])]
    }
    form = FridgeForm(data=data)
    #response = client.post(url_reverse, data=data, content_type='application/x-www-form-urlencoded')
    response = client.post(url_reverse, data=data)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    list_one_missing = soup.find('ol', {'id': "one_missing"})
    list_recipes = soup.find('ol', {'id': "match"})
    recipes_one_missing = list_one_missing.findAll('li')
    assert response.status_code == 200
    assert form.is_valid() is True
    assert len(recipes_one_missing) == 1
    assert list_one_missing.find(string='fridge recipe') is not None
    assert list_recipes is None


@pytest.mark.django_db
def test_plan_activation(client, set_up):
    user = User.objects.all().last()
    client.login(username=user.username, password='fakefake')
    plan = create_fake_plan(user)
    url_reverse = reverse('activate_plan', kwargs={'id': plan.id})
    response = client.get(url_reverse)
    assert response.status_code == 302
    assert UserActivatedPlan.objects.filter(user=user.fitubiuser, plan=plan).exists() is True
    assert UserPlans.objects.filter(user=user.fitubiuser, plan=plan, operation=3).exists() is True

