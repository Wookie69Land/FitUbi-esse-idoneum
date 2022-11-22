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
    ModifyIngredientsToRecipe, RemoveIngredientRecipeView, DeleteRecipeView, \
    AddRecipeToFavouritesView, CreateModifiedRecipeView, CreateRecipeView, \
    RemoveRecipeFromFavouritesView, UtilitiesView, ProfileView, EditProfileView, \
    ChangePasswordView, FavouritesView, FridgeView, PlansView, \
    NewPlanView, PlanModifyView, PlanDetailView, RemoveRecipePlanView

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
    path('modify_ingredients/<int:id>', ModifyIngredientsToRecipe.as_view(), name='recipe_ingredients'),
    path('remove_ingredient/<int:ing_id>/recipe/<int:rec_id>', RemoveIngredientRecipeView.as_view(),
         name='remove_ingredient_recipe'),
    path('delete_recipe/<int:id>', DeleteRecipeView.as_view(), name='delete_recipe'),
    path('add_recipe/<int:id>', AddRecipeToFavouritesView.as_view(), name='add_recipe'),
    path('remove_recipe/<int:id>', RemoveRecipeFromFavouritesView.as_view(), name='remove_recipe'),
    path('new_modified_recipe/<int:id>', CreateModifiedRecipeView.as_view(), name='new_modified_recipe'),
    path('new_recipe/', CreateRecipeView.as_view(), name='new_recipe'),
    path('utilities/', UtilitiesView.as_view(), name='utilities'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('password/', ChangePasswordView.as_view(), name='change_password'),
    path('favourites/', FavouritesView.as_view(), name='favourites'),
    path('fridge/', FridgeView.as_view(), name='fridge'),
    path('plans', PlansView.as_view(), name='plans'),
    path('new_plan/', NewPlanView.as_view(), name='new_plan'),
    path('plans/modify/<int:id>', PlanModifyView.as_view(), name='modify_plan'),
    path('plans/<int:id>/', PlanDetailView.as_view(), name='plan_detail'),
    path('plans/remove/<int:plan_id>/<int:dish_id>', RemoveRecipePlanView.as_view(),
         name='modify_plan'),

]