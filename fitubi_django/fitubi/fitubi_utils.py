
def kilo_to_pound(amount):
    amount_p = round(amount * 2.20462, 3)
    return amount_p


def pound_to_kilo(amount):
    amount_k = round(amount * 0.453592, 3)
    return amount_k


def liter_to_cup(amount):
    amount_c = round(amount * 3.51951, 3)
    return amount_c


def cup_to_liter(amount):
    amount_l = round(amount * 0.284131, 3)
    return amount_l


def liter_to_pint(amount):
    amount_p = round(amount * 1.75975, 3)
    return amount_p


def pint_to_liter(amount):
    amount_l = round(amount * 0.568261, 3)
    return amount_l


def celsius_to_fahrenheit(amount):
    amount_f = (amount * 9/5) + 32
    return amount_f


def fahrenheit_to_celsius(amount):
    amount_c = (amount - 32) * 5/9
    return amount_c




