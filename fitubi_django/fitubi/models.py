from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from multiselectfield import MultiSelectField
from datetime import date

from .choices import *


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
    type = MultiSelectField(choices=DIET_TYPE, max_choices=4, max_length=8)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    objects = RecipeManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/recipe/{self.id}/'

    def calories(self):
        calories = 0
        ingredients = RecipeIngredients.objects.filter(recipe=self)
        for row in ingredients:
            calories += row.ingredient.calories * row.amount
        return calories


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
    name = models.CharField(max_length=128, unique=True)
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

    def calories(self):
        calories = 0
        for recipe in self.recipes.all():
            calories += recipe.calories()
        return round(calories / 7)


class RecipePlanManager(models.Manager):
    def monday(self, plan):
        return self.get_queryset().filter(plan=plan, day=1).order_by('meal')

    def tuesday(self, plan):
        return self.get_queryset().filter(plan=plan, day=2).order_by('meal')

    def wednesday(self, plan):
        return self.get_queryset().filter(plan=plan, day=3).order_by('meal')

    def thursday(self, plan):
        return self.get_queryset().filter(plan=plan, day=4).order_by('meal')

    def friday(self, plan):
        return self.get_queryset().filter(plan=plan, day=5).order_by('meal')

    def saturday(self, plan):
        return self.get_queryset().filter(plan=plan, day=6).order_by('meal')

    def sunday(self, plan):
        return self.get_queryset().filter(plan=plan, day=6).order_by('meal')


class RecipePlan(models.Model):
    day = models.SmallIntegerField(choices=DAYS)
    meal = models.SmallIntegerField(choices=MEALS)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    objects = RecipePlanManager()


class FitUbiUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    food_preference = MultiSelectField(choices=DIET_TYPE, max_length=12, null=True)
    height = models.SmallIntegerField(null=True)
    weight = models.SmallIntegerField(null=True)
    sex = models.SmallIntegerField(choices=SEX, null=True)
    activity = models.SmallIntegerField(choices=ACTIVE_FACTOR, null=True)
    recipes = models.ManyToManyField(Recipe, through='UserRecipes')
    plans = models.ManyToManyField(Plan, through='UserPlans')

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
        conditions = Q(title__icontains=query) | Q(content__icontains=query) | \
                     Q(author__icontains=query) | Q(reference__icontains=query)
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


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sound = models.BooleanField(default=True)
    metric_system = models.SmallIntegerField(choices=UNIT_SYSTEM)


class UserActivatedPlan(models.Model):
    user = models.OneToOneField(FitUbiUser, on_delete=models.CASCADE)
    plan = models.OneToOneField(Plan, on_delete=models.CASCADE)


class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    message = models.TextField()
    recipe = models.ForeignKey(Recipe, blank=True, null=True, on_delete=models.SET_NULL)
    plan = models.ForeignKey(Plan, blank=True, null=True, on_delete=models.SET_NULL)
