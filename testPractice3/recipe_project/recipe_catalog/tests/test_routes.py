from django.test import TestCase, Client
from django.urls import reverse

from ..models import Recipe


class TestRoutes(TestCase):
    def setUp(self):
        self.client = Client()
        self.recipe = Recipe.objects.create(
            name="Овощное рагу",
            desc="Простой рецепт рагу",
            cooking_time="00:45:00"
        )

    def test_index_route(self):
        """Тест главной страницы."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        expected_content = ["Овощное рагу", "Выберите блюдо по вашему вкусу!"]
        for content in expected_content:
            with self.subTest(content=content):
                self.assertContains(response, content)

    def test_about_route(self):
        """Тест страницы 'О нас'."""
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_route(self):
        """Тест страницы рецепта."""
        response = self.client.get(reverse('recipe', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)

        expected_content = [self.recipe.name, self.recipe.desc]
        for content in expected_content:
            with self.subTest(content=content):
                self.assertContains(response, content)

    def test_recipe_detail_404(self):
        """Тест для несуществующего рецепта."""
        response = self.client.get(reverse('recipe', args=[999]))
        self.assertEqual(response.status_code, 404)