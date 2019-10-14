from django.test import TestCase
from rest_framework.utils import json

from recipes.models import Recipe, Ingredient
from rest_framework import status


class RecipeModelTest(TestCase):

    def setUp(self):
        recipe = Recipe.objects.create(name="Pabellon", description="Pabellon description")
        Ingredient.objects.create(recipe=recipe, name="Caraota")
        Ingredient.objects.create(recipe=recipe, name="Carne mechada")
        Ingredient.objects.create(recipe=recipe, name="Arroz")
        Ingredient.objects.create(recipe=recipe, name="Platano")

    def test_create_recipe(self):
        data = {'name': 'Pizza', 'description': 'Pizza description',
                'ingredients': [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]}
        response = self.client.post('/recipes/', content_type='application/json', data=json.dumps(data))
        print(response)
        recipes = Recipe.objects.all()
        self.assertEqual(len(recipes), 2)
        self.assertEqual(json.loads(response.content), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_recipe(self):
        response = self.client.get('/recipes/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_recipe(self):
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_recipe(self):
        data = {'description': 'Pabellon description...'}
        response = self.client.patch('/recipes/1/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(json.loads(response.content), {'name': 'Pabellon',
                                                        'description': 'Pabellon description...',
                                                        'ingredients': [{"name": "Caraota"},
                                                                        {"name": "Carne mechada"},
                                                                        {"name": "Arroz"},
                                                                        {"name": "Platano"}]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_recipe(self):
        response = self.client.delete('/recipes/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)