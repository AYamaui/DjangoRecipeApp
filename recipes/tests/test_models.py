from rest_framework.test import APITestCase
from rest_framework.utils import json

from recipes.models import Recipe, Ingredient
from rest_framework import status


class RecipeModelTest(APITestCase):

    def setUp(self):
        recipe = Recipe.objects.create(name="Pabellon", description="Pabellon description")
        Ingredient.objects.create(recipe=recipe, name="Caraota")
        Ingredient.objects.create(recipe=recipe, name="Carne mechada")
        Ingredient.objects.create(recipe=recipe, name="Arroz")
        Ingredient.objects.create(recipe=recipe, name="Platano")

    def test_create_recipe(self):
        data = {'name': 'Pizza',
                'description': 'Pizza description',
                'ingredients': [{"name": "dough"}, {"name": "cheese"}, {"name": "tomato"}]}
        response = self.client.post('/recipes/', content_type='application/json', data=json.dumps(data))
        recipes = Recipe.objects.all()
        self.assertEqual(len(recipes), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = response.data
        del response['id']
        self.assertEqual(response, data)

        response = self.client.get('/recipes/2/', content_type='application/json')
        response = response.data
        del response['id']
        self.assertEqual(response, data)

    def test_detail_recipe(self):
        data = {
            'id': 1,
            'name': 'Pabellon',
            'description': 'Pabellon description',
            'ingredients': [{"name": "Caraota"},
                            {"name": "Carne mechada"},
                            {"name": "Arroz"},
                            {"name": "Platano"}]
        }
        response = self.client.get('/recipes/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_detail_recipe_not_found(self):
        response = self.client.get('/recipes/2/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_recipe(self):
        data = {
            'id': 1,
            'name': 'Pabellon',
            'description': 'Pabellon description',
            'ingredients': [{"name": "Caraota"},
                            {"name": "Carne mechada"},
                            {"name": "Arroz"},
                            {"name": "Platano"}]
        }
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [data])

    def test_update_recipe(self):
        recipe_id = 1
        data = {
            'name': 'Pabellon',
            'description': 'Pabellon other description...',
            'ingredients': [{"name": "Frijoles negros"},
                            {"name": "Carne mechada"},
                            {"name": "Arroz"}]
        }
        response = self.client.patch('/recipes/{}/'.format(recipe_id),
                                     data=json.dumps(data),
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.data
        del response['id']
        self.assertEqual(response, data)

        response = self.client.get('/recipes/')
        self.assertEqual(response.data["count"], 1)

    def test_delete_recipe(self):
        response = self.client.delete('/recipes/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get('/recipes/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_recipe(self):
        data = {
            'id': 1,
            'name': 'Pabellon',
            'description': 'Pabellon description',
            'ingredients': [{"name": "Caraota"},
                            {"name": "Carne mechada"},
                            {"name": "Arroz"},
                            {"name": "Platano"}]
        }
        response = self.client.get('/recipes/?name=Pa')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [data])

    def test_search_recipe_not_found(self):
        response = self.client.get('/recipes/?name=C')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])