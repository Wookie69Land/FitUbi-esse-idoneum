from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View

import random

from fitubi.models import *
from fitubi.forms import *
from fitubi.fitubi_utils import *


class StartPageView(View):
    def get(self, request):
        return render(request, "start.html")
    def post(self, request):
        if "new-account" in request.POST:
            return redirect("register")
        elif "login" in request.POST:
            return redirect("login")
        else:
            return redirect('main')


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            comment = "Your login or password are invalid. Try again."
            return render(request, "login.html", {'comment': comment})


class NewAccountView(View):
    def get(self, request):
        form_user = UserForm()
        form_fitubi = FitUbiUserForm()
        return render(request, "register.html", {'form_user': form_user, 'form_fitubi': form_fitubi})
    def post(self, request):
        form_user = UserForm(request.POST)
        form_fitubi = FitUbiUserForm(request.POST)
        if form_user.is_valid() and form_fitubi.is_valid():
            username = form_user.cleaned_data.get('username')
            password = form_user.cleaned_data.get('password')
            email = form_user.cleaned_data.get('student')
            new_user = User.objects.create_user(username=username, password=password, email=email)

            new_user.fitubiuser.birth_date = form_fitubi.cleaned_data.get('birth_date')
            new_user.fitubiuser.food_preference = form_fitubi.cleaned_data.get('food_preference')
            new_user.fitubiuser.height = form_fitubi.cleaned_data.get('height')
            new_user.fitubiuser.weight = form_fitubi.cleaned_data.get('weight')
            new_user.fitubiuser.sex = form_fitubi.cleaned_data.get('sex')
            new_user.fitubiuser.activity = form_fitubi.cleaned_data.get('activity')
            new_user.save()

            user = authenticate(username=username, password=password)
            login(request, user)
            comment = "Congratulations! Your can now use FitUbi."
            return render(request, "main.html", {'comment': comment})
        else:
            form_user = UserForm()
            form_fitubi = FitUbiUserForm()
            comment = "Something went wrong. Please try again."
            return render(request, "register.html", {'form_user': form_user, 'form_fitubi': form_fitubi, 'comment': comment})


class MainPageView(View):
    def get(self, request):
        recipes_all = list(Recipe.objects.all())
        random.shuffle(recipes_all)
        recipes_carousel = recipes_all[0:3]
        return render(request, "main.html", {'recipes_carousel': recipes_carousel})
    def post(self, request):
        query = request.POST.get('search')
        recipes = Recipe.objects.search(query)
        return render(request, "recipes_list.html", {'recipes': recipes})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('start')


class RecipesListView(View):
    def get(self, request):
        recipes = Recipe.objects.all().order_by('-updated')
        form = RecipeSearchForm()
        return render(request, "recipes_list.html", {'recipes': recipes,
                                                     'form': form})
    def post(self, request):
        query = request.POST.get('search')
        if query:
            recipes = Recipe.objects.search(query)
        else:
            recipes = Recipe.objects.all()
        form = RecipeSearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('category'):
                category = form.cleaned_data.get('category')
                recipes = recipes.filter(category=category)
            if form.cleaned_data.get('type'):
                type = form.cleaned_data.get('type')
                recipes = recipes.filter(type=type)
        form = RecipeSearchForm()
        return render(request, "recipes_list.html", {'recipes': recipes,
                                                     'form': form})


class RecipeDetailsView(View):
    def get(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        return render(request, "recipe_details.html", {'recipe': recipe})


class ModifyRecipeView(View):
    def get(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        user = request.user
        if recipe.created_by == user:
            form = RecipeForm(instance=recipe)
            return render(request, "recipe_form.html", {'recipe': recipe,
                                                        'form': form})
        comment = "You can modify only recipes created by yourself."
        return render(request, "recipe_details.html", {'recipe': recipe, 'comment': comment})
    def post(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        user = get_object_or_404(FitUbiUser, user=request.user)
        form = RecipeForm(request.POST, instance=recipe)

        if form.is_valid():
            form.save()

            if UserRecipes.objects.filter(user=user, recipe=recipe, operation=2).exists():
                user_recipes = UserRecipes.objects.filter(user=user, recipe=recipe, operation=2)
                user_recipes_update = user_recipes.last()
                user_recipes_update.save()
            else:
                UserRecipes.objects.create(user=user, recipe=recipe, operation=2)

            recipe.refresh_from_db()
            return render(request, "recipe_details.html", {'recipe': recipe})

        form = RecipeForm(instance=recipe)
        return render(request, "recipe_form.html", {'recipe': recipe,
                                                    'form': form})

class AddIngredientsToRecipe(View):
    def get(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        ingredients = Ingredient.objects.all()
        return render(request, "recipe_ingredients_form.html", {'recipe': recipe,
                                                                'ingredients': ingredients})

    def post(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        ingredients = request.POST.getlist('ingredients')
        return render(request, "recipe_details.html", {'recipe': recipe})


