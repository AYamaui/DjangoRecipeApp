from rest_framework import viewsets
from recipes.models import Recipe, Ingredient
from recipes.serializers import RecipeSerializer, IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows to manage recipes
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        """"
        This view should return a list of all the recipes
        """
        name = self.request.query_params.get('name')

        if name:
            return Recipe.objects.filter(name__icontains=name)
        else:
            return self.queryset


class IngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
