from django import forms
from django.forms import ModelForm
from .models import User, FitUbiUser, Ingredient, Recipe, Article, Plan, RecipePlan


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class FitUbiUserForm(ModelForm):
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1930, 2040)))
    class Meta:
        model = FitUbiUser
        fields = ['birth_date', 'food_preference', 'height', 'weight', 'sex']


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "unit", "carbs", "fats", "proteins", "calories", "category", "specials", "dangers"]


class RecipeForm(ModelForm):
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all())
    class Meta:
        model = Recipe
        fields = ["name", 'ingredients', 'description', 'category', 'type']


class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'description']


class RecipePlanForm(ModelForm):
    recipe = forms.ModelMultipleChoiceField(queryset=Recipe.objects.all())
    class Meta:
        model = RecipePlan
        fields = ['day', 'meal', 'recipe']


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'author', 'content', 'reference']
