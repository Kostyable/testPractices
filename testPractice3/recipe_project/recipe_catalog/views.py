from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.checks import messages
from django.db import IntegrityError
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

from .forms import RecipeForm, IngredientForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient, Ingredient


# Create your views here.
def about(request):
    template_name = 'recipe_catalog/about.html'

    return render(request, template_name)

def index(request):
    template_name = 'recipe_catalog/index.html'

    recipes = Recipe.objects.all()

    context = {
        'recipes': recipes.order_by('name')
    }

    return render(request, template_name, context)


def recipe_detail(request, pk):
    template_name = 'recipe_catalog/recipe.html'

    recipe = get_object_or_404(Recipe, pk=pk)
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe).order_by('ingredient__name')

    ingredients = []
    total_cost = 0
    total_raw_weight = 0
    total_processed_weight = 0
    total_calories = 0

    for ri in recipe_ingredients:
        ingredient = ri.ingredient
        quantity = ri.quantity

        if ingredient.unit != "g":
            additional_quantity = ingredient.additional_quantity or 0
            raw_weight = quantity * ingredient.grams_per_unit * additional_quantity
            processed_weight = quantity * ingredient.grams_per_unit * additional_quantity
        else:
            raw_weight = ingredient.raw_weight * quantity or 0
            processed_weight = ingredient.weight * quantity or 0

        ingredients.append({
            'name': ingredient.name,
            'quantity': quantity,
            'raw_weight': raw_weight,
            'processed_weight': processed_weight,
            'cost': ingredient.cost * quantity,
            'calorific': (raw_weight / 100) * ingredient.calorific
        })

        total_cost += ingredient.cost * quantity
        total_raw_weight += raw_weight
        total_processed_weight += processed_weight
        total_calories += (raw_weight / 100) * ingredient.calorific

    context = {
        'title': recipe.name,
        'desc': recipe.desc,
        'recipe_id': pk,
        'ingredients': ingredients,
        'total_cost': total_cost,
        'total_raw_weight': total_raw_weight,
        'total_processed_weight': total_processed_weight,
        'total_calories': total_calories,
        'recipe': recipe
    }

    return render(request, template_name, context)

@login_required
def create_recipe(request):
    template_name = "recipe_catalog/create_recipe.html"
    ingredients = Ingredient.objects.all()
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            ingredient_count = 0
            while f'ingredient_{ingredient_count}' in request.POST:
                ingredient_id = request.POST[f'ingredient_{ingredient_count}']
                quantity = request.POST.get(f'quantity_{ingredient_count}', 1)
                ingredient = Ingredient.objects.get(id=ingredient_id)

                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=int(quantity)
                )

                ingredient_count += 1

            return redirect('/')
    else:
        form = RecipeForm()
    return render(request, template_name, {'form': form, 'ingredients': ingredients})

@login_required
def create_ingredient(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)  # Получаем рецепт по pk
    except Recipe.DoesNotExist:
        raise Http404("Рецепт не найден")

    if request.method == 'POST':
        ingredient_form = IngredientForm(request.POST)

        if ingredient_form.is_valid():
            ingredient = ingredient_form.save()

            quantity = request.POST.get('quantity_0', 1)

            recipe_ingredient = RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity
            )

            return redirect('recipe', pk=recipe.pk)

    else:
        ingredient_form = IngredientForm()

    return render(request, 'recipe_catalog/create_ingredient.html', {
        'ingredient_form': ingredient_form,
        'recipe': recipe,
    })

@login_required
def edit_recipe(request, pk):
    template_name = "recipe_catalog/edit_recipe.html"
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        return HttpResponseForbidden("Вы не являетесь автором этого рецепта.")

    ingredients = Ingredient.objects.all()

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)

        if form.is_valid():
            recipe = form.save()

            deleted_ingredients = request.POST.get('deleted_ingredients', '')
            if deleted_ingredients:
                deleted_ids = map(int, deleted_ingredients.split(','))
                RecipeIngredient.objects.filter(recipe=recipe, id__in=deleted_ids).delete()

            RecipeIngredient.objects.filter(recipe=recipe).delete()

            ingredient_count = 0
            while f'ingredient_{ingredient_count}' in request.POST:
                ingredient_id = int(request.POST[f'ingredient_{ingredient_count}'])
                quantity = int(request.POST.get(f'quantity_{ingredient_count}', 1))
                ingredient = Ingredient.objects.get(id=ingredient_id)

                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=quantity
                )

                ingredient_count += 1

            return redirect('recipe', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, template_name, {'form': form, 'recipe': recipe, 'ingredients': ingredients})




@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот рецепт.")
    if recipe.img:
        recipe.img.delete(save=False)
    recipe.delete()
    return redirect('index')

def signup(request):
    template_name = 'recipe_catalog/signup.html'

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, template_name, {'form': form})

def login(request):
    template_name = 'recipe_catalog/login.html'

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Неверное имя пользователя или пароль")
        else:
            messages.error(request, "Неверные данные")

    else:
        form = AuthenticationForm()
    return render(request, template_name, {'form': form})

def logout(request):
    logout(request)
    return redirect('index')