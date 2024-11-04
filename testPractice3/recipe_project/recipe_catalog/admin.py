from django.contrib import admin

# Register your models here.
from .models import Ingredient, Recipe, RecipeIngredient

class IngredientInline(admin.StackedInline):
    """В рецепте есть ингредиенты"""
    model = RecipeIngredient
    extra = 5

class RecipeAdmin(admin.ModelAdmin):
    """Настройка формы админки для рецепта."""
    inlines = [IngredientInline]
    list_display = ("name", "desc", "img", "cooking_time")

class IngredientAdmin(admin.ModelAdmin):
    """Настройка формы админки для ингредиента."""
    list_display = ("name", "raw_weight", "weight", "cost", "calorific")

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)