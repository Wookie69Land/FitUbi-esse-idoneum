from django.contrib import admin
from .models import FitUbiUser, Recipe, RecipeIngredients, UserRecipes, Ingredient

admin.site.register(FitUbiUser)
admin.site.register(Recipe)
admin.site.register(RecipeIngredients)
admin.site.register(UserRecipes)
admin.site.register(Ingredient)
