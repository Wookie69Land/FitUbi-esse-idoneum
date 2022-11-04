from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver


UNIT = (
    (1, '')
)

FOODCAT = (
    (1, '')
)


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


RECIPE_CATEGORY = (
    (1, '')
)

FOODTYPE = (
    (1, '')
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
    type = models.SmallIntegerField(choices=FOODTYPE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = RecipeManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/articles/{self.id}/'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()
    #unit = models.SmallIntegerField(choices=UNIT)


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

    objects = PlanManager()

    def __str__(self):
        return f"{self.name}"

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
    (1, '')
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
    (3, 'other'),
)


class FitUbiUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    food_preference = models.SmallIntegerField(choices=FOODTYPE)
    height = models.SmallIntegerField()
    weight = models.SmallIntegerField()
    sex = models.SmallIntegerField(choices=SEX)
    favourite_recipes = models.ManyToManyField(Recipe, through='UserRecipes')
    favourite_plans = models.ManyToManyField(Plan, through='UserPlans')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        FitUbiUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class UserRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class UserPlans(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)


class Article(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=64, null=True)
    content = models.TextField()
    reference = models.CharField(max_length=512, null=True)
    slug = models.SlugField(max_length=64, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/articles/{self.slug}/'



