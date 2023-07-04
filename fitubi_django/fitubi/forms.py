from django import forms
from django.forms import ModelForm
from django.core.validators import ValidationError

from fitubi.models import User, FitUbiUser, Ingredient, Recipe, RecipeIngredients, \
    Article, Plan, RecipePlan, UserMessage
from fitubi.fitubi_utils import CONV_OPTIONS
from fitubi.choices import *
from fitubi.tasks import send_message_to_fitubi_task


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
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all().order_by('name'))
    class Meta:
        model = RecipeIngredients
        fields = ['ingredient', 'amount']


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


class BmiForm(forms.Form):
    height = forms.DecimalField(label="Height in centimeters", max_digits=5, decimal_places=1, step_size=0.1)
    weight = forms.DecimalField(label="Weight in kilograms", max_digits=5, decimal_places=1, step_size=0.1)


class FridgeForm(ModelForm):
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all().order_by('name'))
    class Meta:
        model = Recipe
        fields = ['ingredients', 'category', 'type']

    def __init__(self, *args, **kwargs):
        super(FridgeForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = False
        self.fields['type'].required = False


class FitUbiPlanForm(forms.Form):
    meals = forms.MultipleChoiceField(label="pick meals per day: ", choices=MEALS)
    goal = forms.ChoiceField(choices=GOALS, required=False)
    type = forms.ChoiceField(choices=DIET_TYPE, required=False)


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        return "%s" % user.username


class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(pk=self.request.user.id)

    user = CustomModelChoiceField(queryset=None)
    title = forms.CharField(max_length=32)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": "5", 'cols': '20'}))

    def contact(self):
        send_message_to_fitubi_task.delay(self.cleaned_data['user'].username,
                                          self.cleaned_data['title'],
                                          self.cleaned_data['message'])


class MessageForm(ModelForm):
    receiver = forms.ModelChoiceField(queryset=User.objects.all().order_by('username'))
    recipe = forms.ModelChoiceField(queryset=Recipe.objects.all().order_by('-created'))
    plan = forms.ModelChoiceField(queryset=Plan.objects.all().order_by('-created'))
    class Meta:
        model = UserMessage
        fields = ['receiver', 'title', 'message', 'recipe', 'plan']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['recipe'].required = False
        self.fields['plan'].required = False

