# forms.py
from django import forms
from django.forms import modelformset_factory, inlineformset_factory

from .models import Recipe, Ingredient, RecipeIngredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'desc', 'img', 'cooking_time']

class RecipeIngredientForm(forms.ModelForm):
    """Форма для добавления ингредиента в рецепт"""
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity']

    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all(), label="Ингредиент")
    quantity = forms.IntegerField(min_value=1, label="Количество")


class IngredientForm(forms.ModelForm):
    quantity_0 = forms.IntegerField(min_value=1, initial=1, label="Количество", required=True)

    class Meta:
        model = Ingredient
        fields = ['name', 'unit', 'grams_per_unit', 'additional_quantity', 'raw_weight', 'weight', 'cost', 'calorific']
        widgets = {
            'raw_weight': forms.NumberInput(attrs={'step': 'any'}),
            'weight': forms.NumberInput(attrs={'step': 'any'}),
            'grams_per_unit': forms.NumberInput(attrs={'step': 'any'}),
            'cost': forms.NumberInput(attrs={'step': 'any'}),
            'calorific': forms.NumberInput(attrs={'step': 'any'}),
        }
