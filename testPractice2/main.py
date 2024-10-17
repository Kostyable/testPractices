# (Б)линников -> (Б)лины
# (К)онстантин -> (К)арбонара

from pydantic import BaseModel, confloat, constr

class Ingredient(BaseModel):
    name: constr(strip_whitespace=True)
    raw_weight: confloat(gt=0)
    weight: confloat(gt=0)
    cost: confloat(gt=0)
    calorific: confloat(ge=0)

    class Config:
        str_min_length = 2

class Recipe:
    def __init__(self, name, ingredient_list):
        self.name = name
        self.ingredient_list = ingredient_list

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if len(value) < 2:
            raise ValueError("Название рецепта не может состоять менее чем из 2 символов")
        self._name = value

    @property
    def ingredient_list(self):
        return self._ingredient_list

    @ingredient_list.setter
    def ingredient_list(self, lst):
        if len(lst) < 5:
            raise ValueError("В рецепте должно быть не менее 5 ингредиентов")
        self._ingredient_list = lst

    def calculate_weight(self, portions=1, is_raw=True):
        if is_raw:
            total_weight = sum(ingredient.raw_weight for ingredient in self._ingredient_list)
        else:
            total_weight = sum(ingredient.weight for ingredient in self._ingredient_list)
        return total_weight * portions

    def calculate_cost(self, portions=1):
        total_cost = sum(ingredient.cost for ingredient in self._ingredient_list)
        return total_cost * portions

    def calculate_calorific(self, portions=1):
        total_calorific = sum(ingredient.calorific for ingredient in self._ingredient_list)
        return total_calorific * portions

    def __str__(self):
        return f"Рецепт: {self.name}\nИнгредиенты:\n{'\n'.join('- ' + ingredient.name + ', ' + str(ingredient.raw_weight)
                                                               + ' г' for ingredient in self._ingredient_list)}"

if __name__ == '__main__':
    pancakes_recipe_from_api = {
        "title": 'Блины',
        "ingredients_list": [
            ('Молоко', 515, 515, 70, 175),
            ('Яйца (3 шт.)', 180, 180, 40, 210),
            ('Мука', 280, 280, 13, 935),
            ('Сахар', 30, 30, 2.2, 120),
            ('Соль', 7, 7, 0.15, 0),
            ('Растительное масло', 50, 50, 5.75, 450),
            ('Сливочное масло', 25, 25, 27.5, 187.5)
        ]
    }

    pancakes_ingredients = [
        Ingredient(name=name, raw_weight=raw_weight, weight=weight, cost=cost, calorific=calorific)
        for name, raw_weight, weight, cost, calorific in pancakes_recipe_from_api['ingredients_list']
    ]

    pancakes_recipe = Recipe(pancakes_recipe_from_api['title'], pancakes_ingredients)

    carbonara_recipe_from_api = {
        "title": 'Карбонара',
        "ingredients_list": [
            ('Спагетти', 400, 800, 70, 1352),
            ('Бекон', 200, 130, 120, 834),
            ('Яйца (1 целое + 3 желтка)', 120, 120, 53, 250),
            ('Сыр пармезан', 50, 50, 73, 196),
            ('Сливочное масло', 40, 40, 44, 206.25),
            ('Оливковое масло', 15, 15, 20.66, 135),
            ('Соль', 7, 7, 0.15, 0),
            ('Перец чёрный молотый', 3, 3, 8, 7.5)
        ]
    }

    carbonara_ingredients = [
        Ingredient(name=name, raw_weight=raw_weight, weight=weight, cost=cost, calorific=calorific)
        for name, raw_weight, weight, cost, calorific in carbonara_recipe_from_api['ingredients_list']
    ]

    carbonara_recipe = Recipe(carbonara_recipe_from_api['title'], carbonara_ingredients)

    print(pancakes_recipe)
    print(f"Общий вес ингредиентов до готовки: {pancakes_recipe.calculate_weight(is_raw=True)} г")
    print(f"Вес готового блюда: {pancakes_recipe.calculate_weight(is_raw=False)} г")
    print(f"Себестоимость ингредиентов: {pancakes_recipe.calculate_cost()} руб.")
    print(f"Калорийность блюда: {pancakes_recipe.calculate_calorific()} ккал")
    print('-------------------------------------------')
    print(carbonara_recipe)
    print(f"Общий вес ингредиентов до готовки: {carbonara_recipe.calculate_weight(is_raw=True)} г")
    print(f"Вес готового блюда: {carbonara_recipe.calculate_weight(is_raw=False)} г")
    print(f"Себестоимость ингредиентов: {carbonara_recipe.calculate_cost()} руб.")
    print(f"Калорийность блюда: {carbonara_recipe.calculate_calorific()} ккал")