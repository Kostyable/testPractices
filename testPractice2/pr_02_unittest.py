import unittest
from main import Ingredient, Recipe

class TestRecipe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\nSetUpClass: Начало всех тестов")

    def setUp(self):
        self.pancakes_ingredients = [
            Ingredient(name='Молоко', raw_weight=515, weight=515, cost=70, calorific=175),
            Ingredient(name='Яйца (3 шт.)', raw_weight=180, weight=180, cost=40, calorific=210),
            Ingredient(name='Мука', raw_weight=280, weight=280, cost=13, calorific=935),
            Ingredient(name='Сахар', raw_weight=30, weight=30, cost=2.2, calorific=120),
            Ingredient(name='Соль', raw_weight=7, weight=7, cost=0.15, calorific=0),
            Ingredient(name='Растительное масло', raw_weight=50, weight=50, cost=5.75, calorific=450),
            Ingredient(name='Сливочное масло', raw_weight=25, weight=25, cost=27.5, calorific=187.5)
        ]

        self.pancakes_recipe = Recipe("Блины", self.pancakes_ingredients)

        self.carbonara_ingredients = [
            Ingredient(name='Спагетти', raw_weight=400, weight=800, cost=70, calorific=1352),
            Ingredient(name='Бекон', raw_weight=200, weight=130, cost=120, calorific=834),
            Ingredient(name='Яйца', raw_weight=120, weight=120, cost=53, calorific=250),
            Ingredient(name='Сыр пармезан', raw_weight=50, weight=50, cost=73, calorific=196),
            Ingredient(name='Сливочное масло', raw_weight=40, weight=40, cost=44, calorific=206.25),
            Ingredient(name='Оливковое масло', raw_weight=15, weight=15, cost=20.66, calorific=135),
            Ingredient(name='Соль', raw_weight=7, weight=7, cost=0.15, calorific=0),
            Ingredient(name='Перец чёрный молотый', raw_weight=3, weight=3, cost=8, calorific=7.5)
        ]

        self.carbonara_recipe = Recipe("Карбонара", self.carbonara_ingredients)

    def test_calculate_weight_pancakes(self):
        self.assertEqual(self.pancakes_recipe.calculate_weight(is_raw=True), 1087)
        self.assertEqual(self.pancakes_recipe.calculate_weight(is_raw=False), 1087)

    def test_calculate_cost_pancakes(self):
        self.assertEqual(self.pancakes_recipe.calculate_cost(), 158.6)

    def test_calculate_calorific_pancakes(self):
        self.assertEqual(self.pancakes_recipe.calculate_calorific(), 2077.5)

    def test_calculate_weight_carbonara(self):
        self.assertEqual(self.carbonara_recipe.calculate_weight(is_raw=True), 835)
        self.assertEqual(self.carbonara_recipe.calculate_weight(is_raw=False), 1165)

    def test_calculate_cost_carbonara(self):
        self.assertEqual(self.carbonara_recipe.calculate_cost(), 388.81)

    def test_calculate_calorific_carbonara(self):
        self.assertEqual(self.carbonara_recipe.calculate_calorific(), 2980.75)

    def test_invalid_recipe_name(self):
        with self.assertRaises(ValueError):
            Recipe("", self.pancakes_ingredients)

    def test_invalid_ingredient_list(self):
        with self.assertRaises(ValueError):
            Recipe("Invalid", self.pancakes_ingredients[:4])

    def tearDown(self):
        print("Тест завершён")

    @classmethod
    def tearDownClass(cls):
        print("\nTearDownClass: Все тесты завершены")

if __name__ == '__main__':
    unittest.main()