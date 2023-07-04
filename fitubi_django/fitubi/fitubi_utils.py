from .models import RecipeIngredients, RecipePlan, Recipe
import functools
import collections
from playsound import playsound


def kilo_to_stone(amount):
    amount_s = amount / 6.35
    return round(amount_s, 4)


def stone_to_kilo(amount):
    amount_k = amount * 6.35
    return round(amount_k, 4)


def liter_to_gallon(amount):
    amount_g = amount / 3.785
    return round(amount_g, 4)


def gallon_to_liter(amount):
    amount_l = amount * 3.785
    return round(amount_l, 4)


def milliliter_to_pint(amount):
    amount_p = amount / 568.3
    return round(amount_p, 4)


def pint_to_milliliter(amount):
    amount_m = amount * 568.3
    return round(amount_m, 4)


def gram_to_pound(amount):
    amount_p = amount / 453.6
    return round(amount_p, 4)


def pound_to_gram(amount):
    amount_g = amount * 453.6
    return round(amount_g, 4)


def kilo_to_pound(amount):
    amount_p = amount * 2.20462
    return round(amount_p, 4)


def pound_to_kilo(amount):
    amount_k = round(amount * 0.453592, 4)
    return amount_k


def liter_to_cup(amount):
    amount_c = round(amount * 3.51951, 4)
    return amount_c


def cup_to_liter(amount):
    amount_l = round(amount * 0.284131, 4)
    return amount_l


def liter_to_pint(amount):
    amount_p = round(amount * 1.75975, 4)
    return amount_p


def pint_to_liter(amount):
    amount_l = round(amount * 0.568261, 4)
    return amount_l


def celsius_to_fahrenheit(amount):
    amount_f = (amount * 9/5) + 32
    return amount_f


def fahrenheit_to_celsius(amount):
    amount_c = (amount - 32) * 5/9
    return amount_c


def convert_form(operation: int, quantity: float):
    result = 0
    if operation == 1:
        result = kilo_to_pound(quantity)
    elif operation == 2:
        result = pound_to_kilo(quantity)
    elif operation == 3:
        result = liter_to_cup(quantity)
    elif operation == 4:
        result = cup_to_liter(quantity)
    elif operation == 5:
        result = liter_to_pint(quantity)
    elif operation == 6:
        result = pint_to_liter(quantity)
    elif operation == 7:
        result = celsius_to_fahrenheit(quantity)
    elif operation == 8:
        result = fahrenheit_to_celsius(quantity)
    return round(result, 4)


CONV_OPTIONS = (
    (1, 'kilogram to pound'),
    (2, 'pound to kilogram'),
    (3, 'liter to cup'),
    (4, 'cup to liter'),
    (5, 'liter to pint'),
    (6, 'pint to liter'),
    (7, 'celsius to fahrenheit'),
    (8, 'fahrenheit to celsius')
)


def macros_total(recipe):
    macros = {
        'carbs': 0,
        'fats': 0,
        'proteins': 0,
        'calories': 0
    }
    ingredients = RecipeIngredients.objects.filter(recipe=recipe)
    for row in ingredients:
        macros['carbs'] += row.ingredient.carbs * row.amount
        macros['fats'] += row.ingredient.fats * row.amount
        macros['proteins'] += row.ingredient.proteins * row.amount
        macros['calories'] += row.ingredient.calories * row.amount
    return macros


def plan_macros(plan):
    macros = []
    counter = collections.Counter()
    for recipe in plan.recipes.all():
        macros.append(macros_total(recipe))
    for macro in macros:
        counter.update(macro)
    macros = dict(counter)
    for key in macros:
        macros[key] = round(macros[key] / 7, 2)
    return macros


def calculate_bmi(fit_user):
    bmi = fit_user.weight / (fit_user.height/100)**2
    return round(bmi, 4)


def process_bmi(bmi):
    comment = ''
    if bmi <= 18.5:
        comment = 'you are underweight'
    elif 18.5 < bmi <= 24.9:
        comment = 'your weight is healthy'
    elif 24.9 < bmi <= 29.9:
        comment = 'you are overweight'
    elif bmi >= 30:
        comment = 'you are obese'
    return comment


def calculate_bmr(fit_user):
    if fit_user.sex == 1:
        bmr = 10 * fit_user.weight + 6.25 * fit_user.height - 5 * fit_user.get_age() + 5
    elif fit_user.sex == 2:
        bmr = 10 * fit_user.weight + 6.25 * fit_user.height - 5 * fit_user.get_age() - 161
    else:
        bmr = None
    if bmr is not None:
        if fit_user.activity == 1:
            bmr *= 1.2
        elif fit_user.activity == 2:
            bmr *= 1.375
        elif fit_user.activity == 3:
            bmr *= 1.55
        elif fit_user.activity == 4:
            bmr *= 1.725
        elif fit_user.activity == 5:
            bmr *= 1.9
    return round(bmr)


def clean_comment(request):
    if request.session.has_key('comment'):
        del request.session['comment']
    else:
        pass


def coderslab_check(request):
    if request.user.is_authenticated:
        if 'coderslab' in request.user.email:
            coders_surprise = "Welcome member of the CodersLab team. Thank you all for your invaluable help."
            request.session['surprise'] = coders_surprise


def coderslab_playsound(request):
    if request.user.is_authenticated:
        if 'coderslab' in request.user.email:
            playsound('/home/lukasland/Desktop/other_code/FitUbi2/FitUbi-esse-idoneum/fitubi_django/fitubi/static/sounds/rocket.wav')



def surprise(view):
    @functools.wraps(view)
    def wrapper(request, *args, **kwargs):
        email = request.user.email
        if 'coderslab' in email:
            coders_surprise = "Welcome member of the CodersLab team. Thank you all for your invaluable help."
            request.session['surprise'] = coders_surprise
        return view(request, *args, **kwargs)
    return wrapper


def process_plan_week(plan):
    monday = RecipePlan.objects.monday(plan)
    tuesday = RecipePlan.objects.tuesday(plan)
    wednesday = RecipePlan.objects.wednesday(plan)
    thursday = RecipePlan.objects.thursday(plan)
    friday = RecipePlan.objects.friday(plan)
    saturday = RecipePlan.objects.saturday(plan)
    sunday = RecipePlan.objects.sunday(plan)
    return monday, tuesday, wednesday, thursday, friday, saturday, sunday


def check_dish_type(recipe: Recipe, meal: int):
    breakfast_choices = [1, 4, 5, 6, 8, 9, 10, 11, 12]
    brunch_choices = [3, 4, 5, 6, 8, 11, 12]
    snack_choices = [4, 9, 10, 11, 12]
    lunch_choices = [2, 5, 6, 8, 12]
    supper_choices = [4, 6, 8, 10]
    dinner_choices = [5, 6, 8, 10, 12]
    if meal == 1 and recipe.category in breakfast_choices:
        return True
    elif meal == 2 and recipe.category in brunch_choices:
        return True
    elif (meal == 3 or meal == 5) and recipe.category in snack_choices:
        return True
    elif meal == 4 and recipe.category in lunch_choices:
        return True
    elif meal == 6 and recipe.category in supper_choices:
        return True
    elif meal == 7 and recipe.category in dinner_choices:
        return True
    else:
        return False

