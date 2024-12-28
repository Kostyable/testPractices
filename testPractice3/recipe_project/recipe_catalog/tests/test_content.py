from django.db import IntegrityError, transaction
from django.test import TestCase

from ..models import Ingredient, RecipeIngredient, Recipe


class TestContent(TestCase):
    def setUp(self):
        self.ingredient1 = Ingredient.objects.create(
            name="Морковь",
            unit="g",
            grams_per_unit=1.0,
            raw_weight=100.0,
            weight=80.0,
            cost=50.0,
            calorific=40.0
        )
        self.ingredient2 = Ingredient.objects.create(
            name="Картофель (2 шт.)",
            unit="pcs",
            grams_per_unit=150.0,
            additional_quantity=2,
            cost=30.0,
            calorific=80.0
        )

        self.recipe1 = Recipe.objects.create(
            name="Овощное рагу",
            desc="Простой рецепт рагу",
            cooking_time="00:45:00",
            author_id="1"
        )
        self.recipe2 = Recipe.objects.create(
            name="борщ",
            desc="Классический борщ",
            cooking_time="01:00:00",
            author_id="1"
        )

        RecipeIngredient.objects.create(
            recipe=self.recipe1,
            ingredient=self.ingredient1,
            quantity=2
        )
        RecipeIngredient.objects.create(
            recipe=self.recipe1,
            ingredient=self.ingredient2,
            quantity=3
        )
        RecipeIngredient.objects.create(
            recipe=self.recipe2,
            ingredient=self.ingredient1,
            quantity=4
        )
        RecipeIngredient.objects.create(
            recipe=self.recipe2,
            ingredient=self.ingredient2,
            quantity=5
        )

    def test_recipe_creation(self):
        """Проверка создания рецепта и его связи с ингредиентами."""
        recipes = [
            (self.recipe1, "Овощное рагу", "Простой рецепт рагу", "00:45:00"),
            (self.recipe2, "борщ", "Классический борщ", "01:00:00"),
        ]
        for recipe, name, desc, cooking_time in recipes:
            with self.subTest(recipe=recipe.name):
                self.assertEqual(recipe.name, name)
                self.assertEqual(recipe.desc, desc)
                self.assertEqual(recipe.cooking_time, cooking_time)

        recipe_ingredients = [
            (self.recipe1, 2),
            (self.recipe2, 2),
        ]
        for recipe, expected_count in recipe_ingredients:
            with self.subTest(recipe=recipe.name):
                self.assertEqual(RecipeIngredient.objects.filter(recipe=recipe).count(), expected_count)

    def test_ingredient_creation(self):
        """Проверка создания ингредиентов."""
        ingredients = [
            (self.ingredient1, "Морковь", "g", 100.0, 1),
            (self.ingredient2, "Картофель (2 шт.)", "pcs", 0.0, 2),
        ]
        for ingredient, name, unit, raw_weight, additional_quantity in ingredients:
            with self.subTest(ingredient=ingredient.name):
                self.assertEqual(ingredient.name, name)
                self.assertEqual(ingredient.unit, unit)
                self.assertEqual(ingredient.raw_weight, raw_weight)
                self.assertEqual(ingredient.additional_quantity, additional_quantity)

    def test_recipe_ingredient_uniqueness(self):
        """Проверка уникальности связи рецепт-ингредиент."""
        test_cases = [
            {
                "recipe": self.recipe1,
                "ingredient": self.ingredient1,
                "quantity": 1,
            },
            {
                "recipe": self.recipe1,
                "ingredient": self.ingredient2,
                "quantity": 2,
            },
            {
                "recipe": self.recipe2,
                "ingredient": self.ingredient1,
                "quantity": 3,
            },
        ]

        for case in test_cases:
            with self.subTest(recipe=case["recipe"].name, ingredient=case["ingredient"].name):
                try:
                    with transaction.atomic():
                        RecipeIngredient.objects.create(
                            recipe=case["recipe"],
                            ingredient=case["ingredient"],
                            quantity=case["quantity"]
                        )
                except IntegrityError:
                    pass

    def test_recipe_calculations(self):
        """Проверка вычислений в рецепте."""

        calculations = [
            ("Овощное рагу", 190.0, 800.0, 1100.0, 1060.0),
            ("Борщ", 350.0, 1360.0, 1900.0, 1820.0),
        ]

        for recipe_name, expected_cost, expected_calories, expected_raw_weight, expected_weight in calculations:
            recipe = Recipe.objects.get(name=recipe_name)
            recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)

            total_cost = 0
            total_raw_weight = 0
            total_processed_weight = 0
            total_calories = 0

            ingredients = []

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

            with self.subTest(recipe=recipe_name, calculation="cost"):
                self.assertEqual(total_cost, expected_cost)

            with self.subTest(recipe=recipe_name, calculation="calories"):
                self.assertEqual(total_calories, expected_calories)

            with self.subTest(recipe=recipe_name, calculation="raw weight"):
                self.assertEqual(total_raw_weight, expected_raw_weight)

            with self.subTest(recipe=recipe_name, calculation="processed weight"):
                self.assertEqual(total_processed_weight, expected_weight)

    def test_ingredient_without_required_fields(self):
        """Проверка создания ингредиента без обязательных полей, чтобы они принимали значения по умолчанию."""
        ingredient = Ingredient.objects.create(
            name="Огурцы",
            unit="g",
            grams_per_unit=1.0,
            cost=20.0,
            calorific=20.0
        )
        fields = [
            ("weight", ingredient.weight, 0),
            ("raw_weight", ingredient.raw_weight, 0),
            ("additional_quantity", ingredient.additional_quantity, 1),
        ]
        for field, value, expected in fields:
            with self.subTest(field=field):
                self.assertEqual(value, expected)

    def test_ingredient_additional_quantity(self):
        """Проверка использования additional_quantity для ингредиентов."""
        test_cases = [
            {
                "recipe": self.recipe1,
                "ingredient": self.ingredient2,
                "expected_quantity": 3 * self.ingredient2.additional_quantity,
            },
            {
                "recipe": self.recipe2,
                "ingredient": self.ingredient2,
                "expected_quantity": 5 * self.ingredient2.additional_quantity,
            },
            {
                "recipe": self.recipe2,
                "ingredient": self.ingredient1,
                "expected_quantity": 4 * self.ingredient1.additional_quantity,
            },
        ]

        for case in test_cases:
            with self.subTest(recipe=case["recipe"].name, ingredient=case["ingredient"].name):
                ingredient_in_recipe = RecipeIngredient.objects.filter(
                    recipe=case["recipe"], ingredient=case["ingredient"]
                ).first()
                calculated_quantity = ingredient_in_recipe.quantity * case["ingredient"].additional_quantity
                self.assertEqual(calculated_quantity, case["expected_quantity"])

    def test_recipes_sorted_alphabetically(self):
        """Проверка сортировки рецептов в алфавитном порядке."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        recipes = list(response.context["recipes"])
        sorted_recipes = sorted(recipes, key=lambda r: r.name)

        for i, recipe in enumerate(recipes):
            with self.subTest(recipe=recipe.name, index=i):
                self.assertEqual(recipe, sorted_recipes[i])

    def test_ingredients_sorted_alphabetically(self):
        """Проверка сортировки ингредиентов в алфавитном порядке."""
        response = self.client.get(f"/recipe/{self.recipe1.pk}/")
        self.assertEqual(response.status_code, 200)
        ingredients = list(response.context["ingredients"])
        sorted_ingredients = sorted(ingredients, key=lambda i: i["name"])

        for i, ingredient in enumerate(ingredients):
            with self.subTest(ingredient=ingredient["name"], index=i):
                self.assertEqual(ingredient, sorted_ingredients[i])