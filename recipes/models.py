from django.db import models
from django.db.models import CharField, ForeignKey, TextField


class Recipe(models.Model):
    name = CharField(
        max_length=200,
        db_index=True,
        help_text=u"Name of the recipe"
    )

    description = TextField(
        help_text=u"Description od the recipe"
    )

    def __str__(self):
        return '{}: {}, {}'.format(self.name, self.description, self.ingredients)


class Ingredient(models.Model):
    name = CharField(
        max_length=200,
        help_text=u"Name of the ingredient"
    )
    recipe = ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)

    def __str__(self):
        return '{} (Recipe: {})'.format(self.name, self.recipe.id)

