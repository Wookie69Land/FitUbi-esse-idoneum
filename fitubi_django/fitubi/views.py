from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.forms.models import model_to_dict
from django.core.paginator import Paginator

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
        return render(request, "register.html", {'form_user': form_user,
                                                 'form_fitubi': form_fitubi})
    def post(self, request):
        form_user = UserForm(request.POST)
        form_fitubi = FitUbiUserForm(request.POST)
        if form_user.is_valid() and form_fitubi.is_valid():
            username = form_user.cleaned_data.get('username')
            password = form_user.cleaned_data.get('password')
            email = form_user.cleaned_data.get('email')
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
            request.session['comment'] = comment
            return redirect('main')
        else:
            form_user = UserForm()
            form_fitubi = FitUbiUserForm()
            comment = "Something went wrong. Please try again."
            return render(request, "register.html", {'form_user': form_user, 'form_fitubi': form_fitubi, 'comment': comment})


class MainPageView(View):
    def get(self, request):
        coderslab_check(request)
        recipes_all = list(Recipe.objects.all())
        random.shuffle(recipes_all)
        recipes_carousel = recipes_all[0:3]
        return render(request, "main.html", {'recipes_carousel': recipes_carousel})
    def post(self, request):
        query = request.POST.get('query')
        recipes = Recipe.objects.search(query)
        return render(request, "recipes_list.html", {'recipes': recipes})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('start')


class RecipesListView(View):
    def get(self, request):
        clean_comment(request)
        recipes = Recipe.objects.all().order_by('-updated')
        form = RecipeSearchForm()
        paginator = Paginator(recipes, 10)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, "recipes_list.html", {'recipes': recipes,
                                                     'form': form})
    def post(self, request):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})

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
            if form.cleaned_data.get('type') and form.cleaned_data.get('type') != 1:
                type = form.cleaned_data.get('type')
                recipes = recipes.filter(type=type)
        form = RecipeSearchForm()
        paginator = Paginator(recipes, 10)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, "recipes_list.html", {'recipes': recipes,
                                                     'form': form})


class RecipeDetailsView(View):
    def get(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        macros = macros_total(recipe)
        if request.user.is_anonymous:
            return render(request, "recipe_details.html", {'recipe': recipe,
                                                           'macros': macros})

        user = get_object_or_404(FitUbiUser, user=request.user)
        if UserRecipes.objects.filter(user=user, recipe=recipe, operation=1).exists():
            favourite_mark = True
        else:
            favourite_mark = False
        if request.session.has_key('comment'):
            comment = request.session['comment']
            return render(request, "recipe_details.html", {'recipe': recipe,
                                                           'favourite_mark': favourite_mark,
                                                           'macros': macros,
                                                           'comment': comment})
        return render(request, "recipe_details.html", {'recipe': recipe,
                                                       'favourite_mark': favourite_mark,
                                                       'macros': macros})
    def post(self, request):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})


class ModifyRecipeView(LoginRequiredMixin, View):
    def get(self, request, id):
        clean_comment(request)
        recipe = get_object_or_404(Recipe, pk=id)
        user = request.user
        recipe_ingredients = RecipeIngredients.objects.filter(recipe=recipe)
        if recipe.created_by == user:
            form = RecipeForm(instance=recipe)
            return render(request, "recipe_form.html", {'recipe': recipe,
                                                        'form': form,
                                                        'recipe_ingredients': recipe_ingredients})
        comment = "You can modify only recipes created by yourself."
        request.session['comment'] = comment
        url = f'/recipe/{recipe.id}'
        return redirect(url)
    def post(self, request, id):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})

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

            url = f'/recipe/{recipe.id}'
            return redirect(url)

        form = RecipeForm(instance=recipe)
        recipe_ingredients = RecipeIngredients.objects.filter(recipe=recipe)
        return render(request, "recipe_form.html", {'recipe': recipe,
                                                    'form': form,
                                                    'recipe_ingredients': recipe_ingredients})


class ModifyIngredientsToRecipe(LoginRequiredMixin, View):
    def get(self, request, id):
        clean_comment(request)
        recipe = get_object_or_404(Recipe, pk=id)
        ingredients = RecipeIngredients.objects.filter(recipe=recipe)
        form = RecipeIngredientsForm()
        return render(request, "recipe_ingredients_form2.html", {'recipe': recipe,
                                                                 'ingredients': ingredients,
                                                                 'form': form})

    def post(self, request, id):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})

        recipe = get_object_or_404(Recipe, pk=id)
        if 'add' in request.POST:
            form = RecipeIngredientsForm(request.POST)
            if form.is_valid():
                ingredient = form.cleaned_data.get('ingredient')
                amount = form.cleaned_data.get('amount')
                if RecipeIngredients.objects.filter(recipe=recipe, ingredient=ingredient).exists():
                    comment = f'Ingredient already exists in {recipe}.'
                    recipe.refresh_from_db()
                    ingredients = RecipeIngredients.objects.filter(recipe=recipe)
                    form = RecipeIngredientsForm()
                    return render(request, "recipe_ingredients_form2.html", {'recipe': recipe,
                                                                             'ingredients': ingredients,
                                                                             'form': form,
                                                                             'comment': comment})
                RecipeIngredients.objects.create(recipe=recipe,
                                                 ingredient=ingredient,
                                                 amount=amount)
                recipe.refresh_from_db()
                ingredients = RecipeIngredients.objects.filter(recipe=recipe)
                form = RecipeIngredientsForm()
                return render(request, "recipe_ingredients_form2.html", {'recipe': recipe,
                                                                         'ingredients': ingredients,
                                                                         'form': form})
            else:
                comment = 'Submit correct data'
                recipe.refresh_from_db()
                ingredients = RecipeIngredients.objects.filter(recipe=recipe)
                form = RecipeIngredientsForm()
                return render(request, "recipe_ingredients_form2.html", {'recipe': recipe,
                                                                         'ingredients': ingredients,
                                                                         'form': form,
                                                                         'comment': comment})
        if 'convert' in request.POST:
            pass
        if 'finish' in request.POST:
            ingredients = RecipeIngredients.objects.filter(recipe=recipe)
            for row in ingredients:
                row.amount = request.POST.get(str(row.id))
                row.save()
            url = f'/recipe/{recipe.id}'
            return redirect(url)


class RemoveIngredientRecipeView(LoginRequiredMixin, View):
    def get(self, request, ing_id, rec_id):
        ingredient = get_object_or_404(Ingredient, pk=ing_id)
        recipe = get_object_or_404(Recipe, pk=rec_id)
        recipe.ingredients.remove(ingredient)
        return redirect('recipe_ingredients', id=rec_id)


class DeleteRecipeView(LoginRequiredMixin, View):
    def get(self, request, id):
        recipe = get_object_or_404(Recipe, pk=id)
        user = request.user
        if recipe.created_by == user:
            recipe.delete()
            return redirect('recipes_list')
        else:
            comment = "You can delete only recipes created by yourself."
            request.session['comment'] = comment
            url = f'/recipe/{recipe.id}'
            return redirect(url)


class AddRecipeToFavouritesView(LoginRequiredMixin, View):
    def get(self, request, id):
        clean_comment(request)
        recipe = get_object_or_404(Recipe, pk=id)
        user = get_object_or_404(FitUbiUser, user=request.user)
        if UserRecipes.objects.filter(user=user, recipe=recipe, operation=1).exists():
            comment = 'Recipe already in favourites.'
            request.session['comment'] = comment
            url = f'/recipe/{recipe.id}'
            return redirect(url)

        UserRecipes.objects.create(user=user, recipe=recipe, operation=1)
        comment = 'Added recipe to favourites.'
        request.session['comment'] = comment
        url = f'/recipe/{recipe.id}'
        return redirect(url)



class RemoveRecipeFromFavouritesView(LoginRequiredMixin, View):
    def get(self, request, id):
        clean_comment(request)
        recipe = get_object_or_404(Recipe, pk=id)
        user = get_object_or_404(FitUbiUser, user=request.user)
        if UserRecipes.objects.filter(user=user, recipe=recipe, operation=1).exists():
            UserRecipes.objects.filter(user=user, recipe=recipe, operation=1).delete()
            comment = 'Removed recipe from favourites.'
            request.session['comment'] = comment
            url = f'/recipe/{recipe.id}'
            return redirect(url)
        comment = 'Recipe not in favourites.'
        request.session['comment'] = comment
        url = f'/recipe/{recipe.id}'
        return redirect(url)


class CreateModifiedRecipeView(LoginRequiredMixin, View):
    def get(self, request, id):
        clean_comment(request)
        recipe = get_object_or_404(Recipe, pk=id)
        recipe_ingredients = RecipeIngredients.objects.filter(recipe=recipe)
        form = RecipeForm(initial=model_to_dict(recipe, exclude=['id']))
        return render(request, "new_recipe_form.html", {'recipe': recipe,
                                                        'form': form,
                                                        'recipe_ingredients': recipe_ingredients})
    def post(self, request, id):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})

        form = RecipeForm(request.POST)
        recipe = get_object_or_404(Recipe, pk=id)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            category = form.cleaned_data.get('category')
            type = form.cleaned_data.get('type')
            new_recipe = Recipe.objects.create(name=name, description=description,
                                               category=category, type=type, created_by=request.user)
            new_recipe.refresh_from_db()

            ingredients = RecipeIngredients.objects.filter(recipe=recipe)
            for row in ingredients:
                RecipeIngredients.objects.create(recipe=new_recipe, ingredient=row.ingredient,
                                                 amount=row.amount)

            user = get_object_or_404(FitUbiUser, user=request.user)
            UserRecipes.objects.create(user=user, recipe=new_recipe, operation=4)

            url = f'/modify_ingredients/{new_recipe.id}'
            return redirect(url)

        recipe = get_object_or_404(Recipe, pk=id)
        form = RecipeForm(initial=model_to_dict(recipe, exclude=['id']))
        recipe_ingredients = RecipeIngredients.objects.filter(recipe=recipe)
        comment = 'Submit correct data. Remember that name must be unique.'
        return render(request, "new_recipe_form.html", {'recipe': recipe,
                                                        'form': form,
                                                        'recipe_ingredients': recipe_ingredients,
                                                        'comment': comment})


class CreateRecipeView(LoginRequiredMixin, View):
    def get(self, request):
        clean_comment(request)
        form = RecipeForm()
        return render(request, "new_recipe_form.html", {'form': form})
    def post(self, request):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})

        form = RecipeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            category = form.cleaned_data.get('category')
            type = form.cleaned_data.get('type')
            recipe = Recipe.objects.create(name=name, description=description,
                                           category=category, type=type, created_by=request.user)
            recipe.refresh_from_db()

            user = get_object_or_404(FitUbiUser, user=request.user)
            UserRecipes.objects.create(user=user, recipe=recipe, operation=4)

            url = f'/modify_ingredients/{recipe.id}'
            return redirect(url)

        form = RecipeForm()
        comment = 'Submit correct data. Remember that name must be unique.'
        return render(request, "new_recipe_form.html", {'form': form,
                                                        'comment': comment})


class UtilitiesView(View):
    def get(self, request):
        clean_comment(request)
        form = ConverterForm()
        form_bmi = BmiForm()
        return render(request, 'utilities.html', {'form': form,
                                                  'form_bmi': form_bmi})
    def post(self, request):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})

        form_bmi = BmiForm(request.POST)
        form = ConverterForm(request.POST)
        if form.is_valid():
            converter = int(form.cleaned_data.get('converter'))
            quantity = float(form.cleaned_data.get('quantity'))
            result = convert_form(converter, quantity)
            if 'convert' in request.POST:
                initial = {'converter': converter, 'quantity': quantity}
                form = ConverterForm(initial=initial)
                return render(request, 'utilities.html', {'result': result,
                                                          'form': form,
                                                          'form_bmi': form_bmi})
            if 'convert_save' in request.POST:
                request.session['result'] = result
                request.session['converter'] = converter
                return redirect('recipes_list')

        if form_bmi.is_valid():
            height = form_bmi.cleaned_data.get('height')
            weight = form_bmi.cleaned_data.get('weight')
            bmi = weight / (height / 100) ** 2
            bmi = round(bmi, 4)
            return render(request, 'utilities.html', {'bmi': bmi,
                                                      'form': form,
                                                      'form_bmi': form_bmi})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        coderslab_playsound(request)
        bmi = calculate_bmi(user.fitubiuser)
        bmr = calculate_bmr(user.fitubiuser)
        bmi_comment = process_bmi(bmi)
        return render(request, 'profile.html', {'user': user,
                                                'bmi': bmi,
                                                'bmr': bmr,
                                                'bmi_comment': bmi_comment})
    def post(self, request):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form_user = EditUserForm(instance=user)
        form_fitubi = FitUbiUserForm(instance=user.fitubiuser)
        return render(request, 'edit_profile.html', {'form_user': form_user,
                                                     'form_fitubi': form_fitubi})
    def post(self, request):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})

        user = request.user
        form_user = EditUserForm(request.POST, instance=user)
        form_fitubi = FitUbiUserForm(request.POST, instance=user.fitubiuser)
        if form_user.is_valid() and form_fitubi.is_valid():
            form_user.save()
            form_fitubi.save()
            return redirect('profile')
        else:
            form_user = EditUserForm(instance=user)
            form_fitubi = FitUbiUserForm(instance=user.fitubiuser)
            comment = "Check if data is correct"
            return render(request, 'edit_profile.html', {'form_user': form_user,
                                                         'form_fitubi': form_fitubi,
                                                         'comment': comment})


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = UpdatePasswordForm()
        return render(request, 'update_password.html', {'form': form})
    def post(self, request):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})

        user = request.user
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            return redirect('login')


class FavouritesView(LoginRequiredMixin, View):
    def get(self, request):
        user = get_object_or_404(FitUbiUser, user=request.user)
        favourite_recipes = UserRecipes.objects.filter(user=user, operation=1)
        favourite_plans = UserPlans.objects.filter(user=user, operation=1)
        return render(request, 'favourites.html', {'favourite_recipes': favourite_recipes,
                                                   'favourite_plans': favourite_plans})
    def post(self, request):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})


class FridgeView(LoginRequiredMixin, View):
    def get(self, request):
        form = FridgeForm()
        return render(request, 'fridge.html', {'form': form})
    def post(self, request):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})

        form = FridgeForm(request.POST)
        if form.is_valid():
            ingredients = form.cleaned_data.get('ingredients')
            category = form.cleaned_data.get('category')
            type = form.cleaned_data.get('type')

            recipes_all = Recipe.objects.filter(ingredients__in=ingredients).distinct()

            if type:
                for recipe in recipes_all:
                    if type not in recipe.type:
                        recipes_all.exclude(pk=recipe.id)
            if category:
                recipes_all = recipes_all.filter(category=category)

            recipes = []
            recipes_one_missing = []
            for recipe in recipes_all:
                excluded_count = 0
                for ingredient in recipe.ingredients.all():
                    if ingredient not in ingredients:
                        excluded_count += 1
                        if excluded_count > 1:
                            break
                if excluded_count == 0:
                    recipes.append(recipe)
                elif excluded_count == 1:
                    recipes_one_missing.append(recipe)

            return render(request, 'fridge.html', {'form': form,
                                                   'recipes': recipes,
                                                   'recipes_one_missing': recipes_one_missing})
        else:
            form = FridgeForm()
            return render(request, 'fridge.html', {'form': form})


class PlansView(LoginRequiredMixin, View):
    def get(self, request):
        clean_comment(request)
        plans = Plan.objects.all().order_by('-created')
        paginator = Paginator(plans, 5)
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        return render(request, 'plans.html', {'plans': plans})
    def post(self, request):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})

        query = request.POST.get('search')
        if query:
            plans = Plan.objects.search(query)
        else:
            plans = Plan.objects.all()
        paginator = Paginator(plans, 5)
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        return render(request, "plans.html", {'plans': plans})


class NewPlanView(LoginRequiredMixin, View):
    def get(self, request):
        clean_comment(request)
        form = PlanForm()
        return render(request, 'new_plan.html', {'form': form})
    def post(self, request):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})

        form = PlanForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            plan = Plan.objects.create(name=name,
                                       description=description,
                                       created_by=request.user)
            plan.refresh_from_db()

            user = get_object_or_404(FitUbiUser, user=request.user)
            UserPlans.objects.create(user=user, plan=plan, operation=4)

            if "save" in request.POST:
                return redirect('profile')
            url = f'/plans/modify/{plan.id}'
            return redirect(url)

        form = PlanForm()
        comment = 'Submit correct data. Remember that name must be unique.'
        return render(request, "new_plan.html", {'form': form,
                                                 'comment': comment})


class PlanModifyView(LoginRequiredMixin, View):
    def get(self, request, id):
        clean_comment(request)
        plan = get_object_or_404(Plan, pk=id)
        form = PlanForm(instance=plan)
        form_plan_recipe = RecipePlanForm()

        monday, tuesday, wednesday, thursday, friday, saturday, sunday = process_plan_week(plan)
        context = {'plan': plan, 'monday': monday, 'tuesday': tuesday, 'wednesday': wednesday,
                   'thursday': thursday, 'friday': friday, 'saturday': saturday,
                   'sunday': sunday, 'form': form, 'form_plan_recipe': form_plan_recipe}
        return render(request, 'new_plan.html', context=context)
    def post(self, request, id):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})

        plan = get_object_or_404(Plan, pk=id)
        form = PlanForm(request.POST, instance=plan)
        form_plan_recipe = RecipePlanForm(request.POST)

        if form.is_valid() and form_plan_recipe.is_valid():
            form.save()
            day = form_plan_recipe.cleaned_data.get('day')
            meal = form_plan_recipe.cleaned_data.get('meal')
            recipe = form_plan_recipe.cleaned_data.get('recipe')
            RecipePlan.objects.create(day=day, meal=meal, recipe=recipe, plan=plan)
            plan.refresh_from_db()

            user = get_object_or_404(FitUbiUser, user=request.user)
            if UserPlans.objects.filter(user=user, plan=plan, operation=2).exists():
                user_plan = UserPlans.objects.filter(user=user, plan=plan, operation=2)
                user_plan_update = user_plan.last()
                user_plan_update.save()
            else:
                UserPlans.objects.create(user=user, plan=plan, operation=2)

            if "save" in request.POST:
                return redirect('profile')
            url = f'/plans/modify/{plan.id}'
            return redirect(url)

        form = PlanForm(instance=plan)
        form_plan_recipe = RecipePlanForm()
        comment = 'Submit correct data. Remember that name must be unique.'
        monday, tuesday, wednesday, thursday, friday, saturday, sunday = process_plan_week(plan)
        context = {'plan': plan, 'monday': monday, 'tuesday': tuesday, 'wednesday': wednesday,
                   'thursday': thursday, 'friday': friday, 'saturday': saturday, 'sunday': sunday,
                   'form': form, 'form_plan_recipe': form_plan_recipe, 'comment': comment}
        return render(request, 'new_plan.html', context=context)


class PlanDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        plan = get_object_or_404(Plan, pk=id)
        monday, tuesday, wednesday, thursday, friday, saturday, sunday = process_plan_week(plan)

        macros = plan_macros(plan)

        user = get_object_or_404(FitUbiUser, user=request.user)
        if UserPlans.objects.filter(user=user, plan=plan, operation=1).exists():
            favourite_mark = True
        else:
            favourite_mark = False

        context = {'plan': plan, 'monday': monday, 'tuesday': tuesday, 'wednesday': wednesday,
                   'thursday': thursday, 'friday': friday, 'saturday': saturday, 'sunday': sunday,
                   'favourite_mark': favourite_mark, 'macros': macros}
        return render(request, 'plan_detail.html', context=context)
    def post(self, request):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})


class RemoveRecipePlanView(LoginRequiredMixin, View):
    def get(self, request, plan_id, dish_id):
        plan = get_object_or_404(Plan, pk=plan_id)
        dish = get_object_or_404(RecipePlan, pk=dish_id)
        dish.delete()
        url = f'/plans/modify/{plan.id}'
        return redirect(url)


class PlanNewModifiedView(LoginRequiredMixin, View):
    def get(self, request, id):
        clean_comment(request)
        plan = get_object_or_404(Plan, pk=id)
        form = PlanForm(instance=plan)
        form_plan_recipe = RecipePlanForm()

        monday, tuesday, wednesday, thursday, friday, saturday, sunday = process_plan_week(plan)
        context = {'plan': plan, 'monday': monday, 'tuesday': tuesday, 'wednesday': wednesday,
                   'thursday': thursday, 'friday': friday, 'saturday': saturday,
                   'sunday': sunday, 'form': form, 'form_plan_recipe': form_plan_recipe}
        return render(request, 'new_plan.html', context=context)
    def post(self, request, id):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})

        plan = get_object_or_404(Plan, pk=id)
        form = PlanForm(request.POST, instance=plan)
        form_plan_recipe = RecipePlanForm(request.POST)

        if form.is_valid() and form_plan_recipe.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            new_plan = Plan.objects.create(name=name,
                                       description=description,
                                       created_by=request.user)
            new_plan.refresh_from_db()

            plan_dishes = RecipePlan.objects.filter(plan=plan)
            for dish in plan_dishes:
                day = dish.day
                meal = dish.meal
                recipe = dish.recipe
                RecipePlan.objects.create(day=day, meal=meal, recipe=recipe, plan=new_plan)

            day = form_plan_recipe.cleaned_data.get('day')
            meal = form_plan_recipe.cleaned_data.get('meal')
            recipe = form_plan_recipe.cleaned_data.get('recipe')
            RecipePlan.objects.create(day=day, meal=meal, recipe=recipe, plan=new_plan)
            new_plan.refresh_from_db()

            user = get_object_or_404(FitUbiUser, user=request.user)
            UserPlans.objects.create(user=user, plan=new_plan, operation=4)

            if "save" in request.POST:
                return redirect('profile')
            url = f'/plans/modify/{new_plan.id}'
            return redirect(url)

        form = PlanForm(instance=plan)
        form_plan_recipe = RecipePlanForm()
        comment = 'Submit correct data. Remember that name must be unique.'
        monday, tuesday, wednesday, thursday, friday, saturday, sunday = process_plan_week(plan)
        context = {'plan': plan, 'monday': monday, 'tuesday': tuesday, 'wednesday': wednesday,
                   'thursday': thursday, 'friday': friday, 'saturday': saturday, 'sunday': sunday,
                   'form': form, 'form_plan_recipe': form_plan_recipe, 'comment': comment}
        return render(request, 'new_plan.html', context=context)


class AddPlanToFavouritesView(LoginRequiredMixin, View):
    def get(self, request, id):
        clean_comment(request)
        plan = get_object_or_404(Plan, pk=id)
        user = get_object_or_404(FitUbiUser, user=request.user)
        if UserPlans.objects.filter(user=user, plan=plan, operation=1).exists():
            comment = 'Plan already in favourites.'
            request.session['comment'] = comment
            url = f'/plans/{plan.id}'
            return redirect(url)

        UserPlans.objects.create(user=user, plan=plan, operation=1)
        comment = 'Added plan to favourites.'
        request.session['comment'] = comment
        url = f'/plans/{plan.id}'
        return redirect(url)


class RemovePlanFromFavouritesView(LoginRequiredMixin, View):
    def get(self, request, id):
        clean_comment(request)
        plan = get_object_or_404(Plan, pk=id)
        user = get_object_or_404(FitUbiUser, user=request.user)
        if UserPlans.objects.filter(user=user, plan=plan, operation=1).exists():
            UserPlans.objects.filter(user=user, plan=plan, operation=1).delete()
            comment = 'Removed plan from favourites.'
            request.session['comment'] = comment
            url = f'/plans/{plan.id}'
            return redirect(url)
        comment = 'Plan not in favourites.'
        request.session['comment'] = comment
        url = f'/plans/{plan.id}'
        return redirect(url)


class DeletePlanView(LoginRequiredMixin, View):
    def get(self, request, id):
        plan = get_object_or_404(Plan, pk=id)
        user = request.user
        if plan.created_by == user:
            plan.delete()
            return redirect('plans')
        else:
            comment = "You can delete only plans created by yourself."
            request.session['comment'] = comment
            url = f'/plans/{plan.id}'
            return redirect(url)


class ModifyRecipePlanView(LoginRequiredMixin, View):
    def get(self, request, plan_id, meal_id):
        clean_comment(request)
        plan = get_object_or_404(Plan, pk=plan_id)
        dish = get_object_or_404(RecipePlan, pk=meal_id)
        form = PlanForm(instance=plan)
        form_plan_recipe = RecipePlanForm(instance=dish)

        monday, tuesday, wednesday, thursday, friday, saturday, sunday = process_plan_week(plan)
        context = {'plan': plan, 'monday': monday, 'tuesday': tuesday, 'wednesday': wednesday,
                   'thursday': thursday, 'friday': friday, 'saturday': saturday,
                   'sunday': sunday, 'form': form, 'form_plan_recipe': form_plan_recipe}
        return render(request, 'new_plan.html', context=context)
    def post(self, request, plan_id, meal_id):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})

        plan = get_object_or_404(Plan, pk=plan_id)
        dish = get_object_or_404(RecipePlan, pk=meal_id)
        form = PlanForm(request.POST, instance=plan)
        form_plan_recipe = RecipePlanForm(request.POST, instance=dish)

        if form.is_valid() and form_plan_recipe.is_valid():
            form.save()
            form_plan_recipe.save()
            plan.refresh_from_db()

            user = get_object_or_404(FitUbiUser, user=request.user)
            if UserPlans.objects.filter(user=user, plan=plan, operation=2).exists():
                user_plan = UserPlans.objects.filter(user=user, plan=plan, operation=2)
                user_plan_update = user_plan.last()
                user_plan_update.save()
            else:
                UserPlans.objects.create(user=user, plan=plan, operation=2)

            if "save" in request.POST:
                return redirect('profile')
            url = f'/plans/modify/{plan.id}'
            return redirect(url)

        form = PlanForm(instance=plan)
        form_plan_recipe = RecipePlanForm(instance=dish)
        comment = 'Submit correct data. Remember that name must be unique.'
        monday, tuesday, wednesday, thursday, friday, saturday, sunday = process_plan_week(plan)
        context = {'plan': plan, 'monday': monday, 'tuesday': tuesday, 'wednesday': wednesday,
                   'thursday': thursday, 'friday': friday, 'saturday': saturday, 'sunday': sunday,
                   'form': form, 'form_plan_recipe': form_plan_recipe, 'comment': comment}
        return render(request, 'new_plan.html', context=context)


class ActivatePlanView(LoginRequiredMixin, View):
    def get(self, request, id):
        plan = get_object_or_404(Plan, pk=id)
        user = request.user.fitubiuser
        if UserActivatedPlan.objects.filter(user=user).exists():
            active_plan = UserActivatedPlan.objects.get(user=user)
            active_plan.plan = plan
            active_plan.save()
            UserPlans.objects.create(user=user, plan=plan, operation=3)
            return redirect('profile')
        UserActivatedPlan.objects.create(user=user, plan=plan)
        UserPlans.objects.create(user=user, plan=plan, operation=3)
        return redirect('profile')


class AutomaticPlanDecisionView(LoginRequiredMixin, View):
    def get(self, request):
        form = FitUbiPlanForm()
        return render(request, 'plan_decision.html', {'form': form})
    def post(self, request):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})

        form = FitUbiPlanForm(request.POST)
        if form.is_valid():
            meals = form.cleaned_data.get('meals')
            goal = form.cleaned_data.get('goal')
            type = form.cleaned_data.get('type')
            url = '/fitubiplan/'
            for choice in meals:
                url += choice
            url += f'/{goal}/{type}'
            return redirect(url)


class AutomaticPlanView(LoginRequiredMixin, View):
    def get(self, request, meals, goal, type):
        clean_comment(request)
        fit_user = get_object_or_404(FitUbiUser, user=request.user)
        meals = [int(m) for m in str(meals)]
        daily_calories = calculate_bmr(fit_user)
        calories_limit = daily_calories
        if goal == 1:
            calories_limit = daily_calories * 0.8
        elif goal == 2:
            calories_limit = daily_calories * 0.9
        elif goal == 4:
            calories_limit = daily_calories * 1.1
        elif goal == 5:
            calories_limit = daily_calories * 1.2
        calories_dish_limit = calories_limit / len(meals)

        goal_description = GOALS[goal-1][1]

        name = f'FitUbi plan for {request.user}'
        description = f'Random plan tailored for {request.user} to {goal_description}'

        if Plan.objects.filter(name=name).exists():
            get_object_or_404(Plan, name=name).delete()
        plan = Plan.objects.create(name=name, description=description, created_by=request.user)

        if type != 1:
            recipes = Recipe.objects.filter(type=type).order_by('?')
        else:
            recipes = Recipe.objects.all().order_by('?')

        for day in DAYS:
            for meal in meals:
                for recipe in recipes:
                    if recipe not in plan.recipes.all():
                        if calories_dish_limit * 0.9 < macros_total(recipe)['calories'] <= calories_dish_limit * 1.1 \
                                and check_dish_type(recipe, meal) == True:
                            RecipePlan.objects.create(day=day[0], meal=meal, recipe=recipe, plan=plan)
                            break

        url = f'/plans/{plan.id}'
        return redirect(url)


class ContactView(LoginRequiredMixin, View):
    def get_form_kwargs(self):
        kwargs = super(ContactView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get(self, request):
        form = ContactForm(request=request)
        return render(request, 'contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST, request=request)
        if form.is_valid():
            form.contact()
            user = form.cleaned_data.get('user')
            title = form.cleaned_data.get('title')
            message = form.cleaned_data.get('message')
            UserMessage.objects.create(sender=user, receiver_id=1, title=title, message=message)
            comment = "Thank you for contacting FitUbi."
            request.session['comment'] = comment
            return redirect('profile')
        else:
            form = ContactForm(request=request)
            return render(request, 'contact.html', {'form': form})


class UserMessagesView(LoginRequiredMixin, View):
    def get(self, request):
        messages_from = UserMessage.objects.filter(sender=request.user).order_by('-created')
        messages_to = UserMessage.objects.filter(receiver=request.user).order_by('-created')
        return render(request, 'messages.html', {'messages_from': messages_from,
                                                 'messages_to': messages_to})
    def post(self, request):
        if request.POST.get('query'):
            query = request.POST.get('query')
            recipes = Recipe.objects.search(query)
            return render(request, "recipes_list.html", {'recipes': recipes})


class MessageView(LoginRequiredMixin, View):
    def get(self, request, id):
        user_message = get_object_or_404(UserMessage, pk=id)
        if user_message.receiver == request.user or user_message.sender == request.user:
            if user_message.receiver == request.user:
                user_message.read = True
                user_message.save()
            return render(request, 'message_details.html', {'user_message': user_message})
        else:
            comment = "You can read only your messages."
            request.session['comment'] = comment
            return redirect('profile')

