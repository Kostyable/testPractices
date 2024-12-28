import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class Ingredient(models.Model):
    """Составная часть рецепта."""
    UNIT_CHOICES = [
        ("g", "граммы"),
        ("ml", "миллилитры"),
        ("pcs", "штуки"),
        ("tsp", "чайные ложки"),
        ("tbsp", "столовые ложки"),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default="g",
        verbose_name="Единица измерения"
    )
    grams_per_unit = models.DecimalField(
        max_digits=10, decimal_places=3,
        verbose_name="Грамм на единицу измерения"
    )
    additional_quantity = models.IntegerField(
        null=False, default=1, blank=True, verbose_name="Количество"
    )
    raw_weight = models.DecimalField(
        max_digits=10, decimal_places=3,
        null=False, default=0, blank=True, verbose_name="Сырой вес, г"
    )
    weight = models.DecimalField(
        max_digits=10, decimal_places=3,
        null=False, default=0, blank=True, verbose_name="Вес после обработки, г"
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2,
                               verbose_name="Стоимость, руб"
                               )
    calorific = models.DecimalField(max_digits=10, decimal_places=2,
                                    verbose_name="Калорийность (на 100 г), ккал"
                                    )

    def clean(self):
        """Проверка валидности данных перед сохранением."""
        if self.unit == "g":
            if not self.raw_weight or not self.weight:
                raise ValidationError(
                    "Для единицы измерения 'граммы' поля 'сырой вес' и 'вес после обработки' обязательны.")
        super().clean()

    def __str__(self):
        return self.name

class Recipe(models.Model):
    """Вкусное делается по рецепту."""
    name = models.CharField(max_length=300, verbose_name="Название")
    desc = models.CharField(max_length=1000, verbose_name="Описание")
    img = models.ImageField(blank=True, null=True, verbose_name="Изображение")
    cooking_time = models.TimeField(default=datetime.time(0, 30, 0),
                                    verbose_name="Время приготовления")
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name="recipes")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:
            old_recipe = Recipe.objects.get(pk=self.pk)
            if old_recipe.img and old_recipe.img != self.img:
                old_recipe.img.delete(save=False)
        super().save(*args, **kwargs)

class RecipeIngredient(models.Model):
    """Связь между рецептом и ингредиентом."""
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE
    )
    quantity = models.IntegerField(
        default=1, verbose_name="Количество"
    )

    def __str__(self):
        return f'{self.recipe.name} - {self.ingredient.name} (Количество: {self.quantity})'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique recipes ingredients'
            )
        ]