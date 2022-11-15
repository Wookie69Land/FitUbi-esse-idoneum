from django.contrib import admin
from fitubi.models import FitUbiUser, Recipe, RecipeIngredients

admin.site.register(FitUbiUser)
admin.site.register(Recipe)
admin.site.register(RecipeIngredients)
