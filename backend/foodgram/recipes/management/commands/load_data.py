import json
import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from recipes.models import Ingredient, Tag, Recipe, RecipesIngredient, RecipesTag
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Load JSON ingredients and tags data'

    def handle(self, *args, **options):
        with open('data/ingredients.json') as ingredients_data:
            ingredients = json.load(ingredients_data)
        for ingredient in ingredients:
            try:
                Ingredient.objects.get_or_create(**ingredient)
            except IntegrityError:
                continue

        with open('data/tags.json') as tags_data:
            tags = json.load(tags_data)
        for tag in tags:
            try:
                Tag.objects.get_or_create(**tag)
            except IntegrityError:
                continue

        with open('data/users.json') as users_data:
            users = json.load(users_data)
            for user in users:
                try:
                    CustomUser.objects.get_or_create(**user)
                except IntegrityError:
                    continue

        with open('data/recipes.json') as recipes_data:
            recipes = json.load(recipes_data)
            users_count = CustomUser.objects.count()
            for recipe in recipes:
                recipe_ingredients = recipe.pop('ingredients')
                recipe_tags = recipe.pop('tags')
                random_id = random.randint(1, users_count - 1)
                author = CustomUser.objects.get(id=random_id)
                try:
                    new_recipe = Recipe.objects.create(author=author, **recipe)
                except IntegrityError:
                    continue
                for ingredient in recipe_ingredients:
                    ingredient_obj = Ingredient.objects.get(id=ingredient['id'])
                    RecipesIngredient.objects.create(ingredient=ingredient_obj, recipe=new_recipe, amount=ingredient['amount'])

                for tag in recipe_tags:
                    tag_obj = Tag.objects.get(id=tag)
                    RecipesTag.objects.create(tag=tag_obj, recipe=new_recipe)
                