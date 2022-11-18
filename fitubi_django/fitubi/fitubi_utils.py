from fitubi.models import RecipeIngredients


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


def calculate_bmi(fit_user):
    bmi = fit_user.weight / (fit_user.height/100)**2
    return bmi


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
    return bmr


def clean_comment(request):
    if request.session.has_key('comment'):
        del request.session['comment']
    else:
        pass



