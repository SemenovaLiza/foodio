import json
import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from recipes.models import (
    Ingredient, Tag, Recipe,
    RecipesIngredient, RecipesTag
)
from users.models import CustomUser


# abstract function for loading data from json file
def load_data(data, obj_class, stdout=None, style=None):
    try:
        with open(str(data)) as data_:
            objects = json.load(data_)
            for obj in objects:
                try:
                    obj_class.objects.get_or_create(**obj)
                except IntegrityError:
                    continue
    except (FileNotFoundError, json.JSONDecodeError):
        stdout.write(style.ERROR("Error occured while loading the data."))


class Command(BaseCommand):
    help = 'Load JSON ingredients and tags data'

    def handle(self, *args, **options):
        load_data('data/ingredients.json', Ingredient, self.stdout, self.style)
        load_data('data/tags.json', Tag, self.stdout, self.style)
        load_data('data/users.json', CustomUser, self.stdout, self.style)

        with open('data/recipes.json') as recipes_data:
            recipes = json.load(recipes_data)
            for recipe in recipes:
                recipe_ingredients = recipe.pop('ingredients')
                recipe_tags = recipe.pop('tags')
                user_ids = list(CustomUser.objects.values_list('id', flat=True))
                try:
                    random_id = random.choice(user_ids)
                    author = CustomUser.objects.get(id=random_id)
                    new_recipe = Recipe.objects.create(author=author, **recipe)
                except IntegrityError:
                    continue
                for ingredient in recipe_ingredients:
                    ingredient_obj = Ingredient.objects.get(id=ingredient['id'])
                    RecipesIngredient.objects.create(
                        ingredient=ingredient_obj, recipe=new_recipe,
                        amount=ingredient['amount']
                    )

                for tag in recipe_tags:
                    tag_obj = Tag.objects.get(id=tag)
                    RecipesTag.objects.create(tag=tag_obj, recipe=new_recipe)
        self.stdout.write(
            self.style.SUCCESS("Data loading completed successfully.")
        )
