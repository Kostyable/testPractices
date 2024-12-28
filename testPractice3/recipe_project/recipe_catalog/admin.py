from django.contrib import admin

# Register your models here.
from .models import Ingredient, Recipe, RecipeIngredient

class IngredientInline(admin.TabularInline):
    """В рецепте есть ингредиенты"""
    model = RecipeIngredient
    extra = 5
    fields = ['ingredient', 'quantity']

class RecipeAdmin(admin.ModelAdmin):
    """Настройка формы админки для рецепта."""
    inlines = [IngredientInline]
    list_display = ("name", "desc", "img", "cooking_time")

class IngredientAdmin(admin.ModelAdmin):
    """Настройка формы админки для ингредиента."""
    list_display = ("name", "unit", "grams_per_unit", "additional_quantity", "raw_weight", "weight", "cost",
                    "calorific")
    fields = ("name", "unit", "grams_per_unit", "additional_quantity", "raw_weight", "weight", "cost", "calorific")

    class Media:
        js = ('admin/js/custom_admin.js',)

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)