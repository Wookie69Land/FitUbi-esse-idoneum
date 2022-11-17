from django import forms
from django.forms import ModelForm
from .models import User, FitUbiUser, DIET_TYPE, Ingredient, Recipe, RecipeIngredients, Article, Plan, RecipePlan


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class LoginForm2(forms.Form):
    login = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class FitUbiUserForm(ModelForm):
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1930, 2040)))
    food_preference = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DIET_TYPE)
    class Meta:
        model = FitUbiUser
        fields = ['birth_date', 'food_preference', 'height', 'weight', 'sex', 'activity']


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "unit", "carbs", "fats", "proteins", "calories", "category", "specials", "dangers"]


class RecipeForm(ModelForm):
    type = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DIET_TYPE)
    class Meta:
        model = Recipe
        fields = ["name", 'description', 'category', 'type']


class RecipeIngredientsForm(ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = ['ingredient', 'amount']
    def __init__(self, *args, **kwargs):
        super(RecipeIngredientsForm, self).__init__(*args, **kwargs)
        self.fields['ingredient'].required = False
        self.fields['amount'].required = False


class RecipeSearchForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['category', 'type']

    def __init__(self, *args, **kwargs):
        super(RecipeSearchForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['type'].required = False


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
