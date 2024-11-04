from django.shortcuts import render
from .models import Recipe

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

    recipe = Recipe.objects.get(pk=pk)
    context = {
        'title': recipe.name,
        'desc': recipe.desc,
        'recipe_id': pk,
        'ingredients': recipe.ingredients.order_by('name')
    }

    return render(request, template_name, context)