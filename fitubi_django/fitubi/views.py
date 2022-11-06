from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.views import View
from .models import User
from .forms import *


class StartPageView(View):
    def get(self, request):
        return render(request, "start.html")
    def post(self, request):
        if "new-account" in request.POST:
            return redirect("register")
        elif "login" in request.POST:
            return redirect('login')
        else:
            return render(request, "main.html")


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return HttpResponse("login success")
        else:
            comment = "Your login or password are invalid. Try again."
            return render(request, "login.html", {'comment': comment})


class NewAccountView(View):
    def get(self, request):
        form_user = UserForm(instance=request.user)
        form_fitubi = FitUbiUserForm(instance=request.user.fitubiuser)
        return render(request, "register.html", {'form_user': form_user, 'form_fitubi': form_fitubi})



