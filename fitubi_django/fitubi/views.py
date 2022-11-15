from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth import authenticate, login
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


class RecipesListView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        form = RecipeForm()
        return render(request, "recipes_list.html", {'recipes': recipes, 'form': form})
    def post(self, request):
        query = request.POST.get('search')
        if query:
            recipes = Recipe.objects.search(query)
        return render(request, "recipes_list.html", {'recipes': recipes})




