from django import forms
from django.forms import ModelForm
from django.core.validators import ValidationError

from .models import User, FitUbiUser, DIET_TYPE, Ingredient, Recipe, RecipeIngredients, Article, Plan, RecipePlan
from fitubi.fitubi_utils import CONV_OPTIONS


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data.get('username')).exists():
            raise ValidationError('This login is already taken')
        return self.cleaned_data.get('username')

    def clean_password2(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise ValidationError('Passwords do not match!')
        return self.cleaned_data.get('password2')


class UpdatePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    def clean_password_repeat(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise ValidationError('Passwords do not match!')
        return self.cleaned_data.get('password2')


class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


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
    recipe = forms.ModelChoiceField(queryset=Recipe.objects.all())
    class Meta:
        model = RecipePlan
        fields = ['day', 'meal', 'recipe']


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'author', 'content', 'reference']


class ConverterForm(forms.Form):
    converter = forms.ChoiceField(choices=CONV_OPTIONS)
    quantity = forms.DecimalField(max_digits=10, decimal_places=2, step_size=0.1)


class FridgeForm(ModelForm):
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all().order_by('name'))
    class Meta:
        model = Recipe
        fields = ['ingredients', 'category', 'type']

    def __init__(self, *args, **kwargs):
        super(FridgeForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['type'].required = False
