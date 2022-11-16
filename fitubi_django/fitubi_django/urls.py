"""fitubi_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fitubi.views import StartPageView, LoginView, NewAccountView, MainPageView, \
    RecipesListView, LogoutView, RecipeDetailsView, ModifyRecipeView, \
    AddIngredientsToRecipe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', StartPageView.as_view(), name='start'),
    path('login/', LoginView.as_view(), name='login'),
    path('new_account/', NewAccountView.as_view(), name='register'),
    path('main/', MainPageView.as_view(), name='main'),
    path('recipes/', RecipesListView.as_view(), name='recipes_list'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('recipe/<int:id>/', RecipeDetailsView.as_view(), name='recipe_details'),
    path('modify_recipe/<int:id>/', ModifyRecipeView.as_view(), name='modify_recipe'),
    path('modify_ingredients/<int:id>', AddIngredientsToRecipe.as_view(), name='recipe-ingredients'),
]
