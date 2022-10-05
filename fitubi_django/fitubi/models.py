from django.db import models

class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=64)
    birth_date = models.DateField()
    food_preference = models.SmallIntegerField(choices=FOODTYPE)
    active = models.SmallIntegerField(choices=ACTIVE)
    height = models.SmallIntegerField()
    weight = models.SmallIntegerField()
    sex = models.SmallIntegerField(choices=SEX)
    #favourites
    #plans

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    unit = models.SmallIntegerField(choices=UNIT)
    #unit2 = models.SmallIntegerField(choices=UNIT)
    carbs = models.IntegerField()
    fats = models.IntegerField()
    proteins = models.IntegerField()
    calories = models.IntegerField()
    category = models.SmallIntegerField(choices=FOODCAT)
    specials = models.TextField(null=True)
    dangers = models.TextField(null=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=128, unique=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredients')
    description = models.TextField()
    category = models.SmallIntegerField(choices=REC_CATEGORY)
    type = models.SmallIntegerField(choices=FOODTYPE)

    def __str__(self):
        return self.name

class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()
    #unit = models.SmallIntegerField(choices=UNIT)

class Article(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=64, null=True)
    content = models.TextField()
    reference = models.CharField(max_length=512)

    def __str__(self):
        return self.title

