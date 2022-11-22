from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from multiselectfield import MultiSelectField
from datetime import date


UNIT = (
    (1, 'kilogram'),
    (2, 'liter'),
    (3, 'cup'),
    (4, 'pinch'),
    (5, 'tablespoon'),
    (6, 'teaspoon'),
    (7, 'pint'),
    (8, 'pound'),
)

FOODCAT = (
    (1, 'other'),
    (2, 'dairy and eggs'),
    (3, 'vegetables'),
    (4, 'fruits'),
    (5, 'spices and herbs'),
    (6, 'oils and fats'),
    (7, 'flours and starches'),
    (8, 'grains'),
    (9, 'nuts and seeds'),
    (10, 'meat'),
    (11, 'legumes'),
    (12, 'fishes and seafood'),
    (13, 'pasta, rice and pulses'),
)


class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True)
    unit = models.SmallIntegerField(choices=UNIT)
    carbs = models.IntegerField()
    fats = models.IntegerField()
    proteins = models.IntegerField()
    calories = models.IntegerField()
    category = models.SmallIntegerField(choices=FOODCAT)
    specials = models.TextField(null=True)
    dangers = models.TextField(null=True)

    def __str__(self):
        return f'{self.name} in {self.get_unit_display()}'


RECIPE_CATEGORY = (
    (1, 'breakfast'),
    (2, 'lunch'),
    (3, 'beverage'),
    (4, 'appetizer'),
    (5, 'soup'),
    (6, 'salad'),
    (7, 'main dish'),
    (8, 'side dish'),
    (9, 'dessert'),
    (10, 'snack'),
    (11, 'baked-good'),
    (12, 'holiday'),
    (13, 'sauces and dips')
)

DIET_TYPE = (
    (1, 'standard'),
    (2, 'vegan'),
    (3, 'vegetarian'),
    (4, 'pescetarian'),
    (5, 'keto'),
    (6, 'carnivore'),
)


class RecipeManager(models.Manager):
    def search(self, query=None):
        if query is None or query == "":
            return self.get_queryset().none()
        conditions = Q(name__icontains=query) | Q(description__icontains=query)
        return self.get_queryset().filter(conditions)


class Recipe(models.Model):
    name = models.CharField(max_length=128, unique=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredients')
    description = models.TextField()
    category = models.SmallIntegerField(choices=RECIPE_CATEGORY)
    type = MultiSelectField(choices=DIET_TYPE, max_choices=4, max_length=4)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    objects = RecipeManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/recipe/{self.id}/'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return f'{self.recipe}: {self.ingredient}'


class PlanManager(models.Manager):
    def search(self, query=None):
        if query is None or query == "":
            return self.get_queryset().none()
        conditions = Q(name__icontains=query) | Q(description__icontains=query)
        return self.get_queryset().filter(conditions)


class Plan(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    recipes = models.ManyToManyField(Recipe, through='RecipePlan')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    objects = PlanManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/plans/{self.id}/'


DAYS = (
    (1, 'Poniedziałek'),
    (2, 'Wtorek'),
    (3, 'Środa'),
    (4, 'Czwartek'),
    (5, 'Piątek'),
    (6, 'Sobota'),
    (7, 'Niedziela'),
)


MEALS = (
    (1, 'breakfast'),
    (2, 'brunch'),
    (3, 'snack 1'),
    (4, 'lunch'),
    (5, 'snack 2'),
    (6, 'supper'),
    (7, 'dinner'),
)


class RecipePlan(models.Model):
    day = models.SmallIntegerField(choices=DAYS)
    meal = models.SmallIntegerField(choices=MEALS)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def get_plan_by_day(self, day):
        return self.objects.filter(day=day).order_by("meal")


SEX = (
    (1, 'man'),
    (2, 'woman'),
)


ACTIVE_FACTOR = (
    (1, "sedentary: little or no exercise, desk job"),
    (2, "lightly active: exercise 1-3 times per week"),
    (3, "moderately active: exercise 6-7 time per week"),
    (4, "very active: hard exercise every day"),
    (5, "extra active: training for marathon or triathlon")
)


class FitUbiUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    food_preference = MultiSelectField(choices=DIET_TYPE, max_length=6, null=True)
    height = models.SmallIntegerField(null=True)
    weight = models.SmallIntegerField(null=True)
    sex = models.SmallIntegerField(choices=SEX, null=True)
    activity = models.SmallIntegerField(choices=ACTIVE_FACTOR, null=True)
    favourite_recipes = models.ManyToManyField(Recipe, through='UserRecipes')
    favourite_plans = models.ManyToManyField(Plan, through='UserPlans')

    def __str__(self):
        return self.user.username

    def get_age(self):
        today = date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return age


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        FitUbiUser.objects.create(user=instance)
    instance.fitubiuser.save()


OPERATIONS = (
    (1, 'add to favourites'),
    (2, 'modify'),
    (3, 'delete'),
    (4, 'create')
)


class UserRecipes(models.Model):
    user = models.ForeignKey(FitUbiUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    operation = models.SmallIntegerField(choices=OPERATIONS)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class UserPlans(models.Model):
    user = models.ForeignKey(FitUbiUser, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    operation = models.SmallIntegerField(choices=OPERATIONS)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class ArticleManager(models.Manager):
    def search(self, query=None):
        if query is None or query == "":
            return self.get_queryset().none()
        conditions = Q(title__icontains=query) | Q(content__icontains=query) | Q(author__icontains=query)
        return self.get_queryset().filter(conditions)


class Article(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=64, null=True)
    content = models.TextField()
    reference = models.CharField(max_length=512, null=True)
    slug = models.SlugField(max_length=64, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ArticleManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/articles/{self.slug}/'



