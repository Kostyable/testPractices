import datetime

from django.db import models

# Create your models here.
class Ingredient(models.Model):
    """Составная часть рецепта."""
    name = models.CharField(max_length=255)
    raw_weight = models.DecimalField(max_digits=10, decimal_places=3)
    weight = models.DecimalField(max_digits=10, decimal_places=3)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    calorific = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    """Вкусное делается по рецепту."""
    name = models.CharField(max_length=300)
    desc = models.CharField(max_length=1000)
    img = models.ImageField()
    cooking_time = models.TimeField(default=datetime.time(0, 30, 0))
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient")

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    """Один ингредиент может быть
    в нескольких рецептах,
    как и в одном рецепте может быть
    несколько ингредиентов."""
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique recipes ingredients'
            )
        ]