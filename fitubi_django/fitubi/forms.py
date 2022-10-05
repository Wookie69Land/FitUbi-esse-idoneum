from django import forms
from django.forms import ModelForm
from fitubi.models import User, Ingredient, Recipe, Article

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['name', 'password', 'age', 'food_preference', 'active', 'height', 'weight', 'sex']

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "unit", "carbs", "fats", "proteins", "calories", "category", "specials", "dangers"]

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", 'ingredients', 'description', 'category', 'type']

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'author', 'content', 'reference']
