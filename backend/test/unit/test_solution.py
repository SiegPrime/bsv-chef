import pytest
from unittest.mock import MagicMock
from src.controllers.recipecontroller import RecipeController
from src.util.dao import DAO
from src.static.diets import Diet

@pytest.fixture
def recipe_controller():
    dao = MagicMock(spec=DAO)
    controller = RecipeController(items_dao=dao)
    controller.load_recipes = MagicMock(return_value=[
        {
            "name": "Banana Bread",
            "diets": ["normal", "vegetarian"],
            "ingredients": {
                "Butter": 100,
                "Banana": 4,
                "Sugar": 200,
                "Egg": 1,
                "Vanilla Sugar": 1,
                "Baking Powder": 0.5,
                "Salt": 5,
                "Cinnamon": 10,
                "Flour": 220,
                "Walnuts": 10
            }
        },
        {
            "name": "Pancakes",
            "diets": ["normal", "vegetarian"],
            "ingredients": {
                "Egg": 3,
                "Milk": 100,
                "Yoghurt": 200,
                "Flour": 150,
                "Baking Powder": 1,
                "Salt": 5,
                "Sugar": 25
            }
        },
        {
            "name": "Whole Grain Bread",
            "diets": ["normal", "vegetarian", "vegan"],
            "ingredients": {
                "Flour": 500,
                "Walnuts": 20,
                "Yeast": 1,
                "Salt": 10,
                "Vinegar": 30
            }
        }
    ])
    controller.recipes = controller.load_recipes()
    controller.get_available_items = MagicMock(return_value={"Flour": 500, "Walnuts": 20, "Yeast": 1, "Salt": 10, "Vinegar": 30})
    controller.get_recipe_readiness = MagicMock(side_effect=lambda recipe, items, diet: 1.0 if recipe['name'] == "Whole Grain Bread" else 0.5)
    return controller

@pytest.mark.unit
def test_get_recipe_best_single(recipe_controller):
    recipe = recipe_controller.get_recipe(Diet.VEGAN, True)
    assert recipe == "Whole Grain Bread"

@pytest.mark.unit
def test_get_recipe_random_single(recipe_controller):
    recipe = recipe_controller.get_recipe(Diet.VEGETARIAN, False)
    assert recipe in ["Banana Bread", "Pancakes", "Whole Grain Bread"]

@pytest.mark.unit
def test_get_recipe_no_valid_readiness(recipe_controller):
    recipe_controller.get_recipe_readiness = MagicMock(return_value=None)
    recipe = recipe_controller.get_recipe(Diet.VEGAN, True)
    assert recipe is None

#The same result as above.
@pytest.mark.unit
def test_get_recipe_no_diet_compliance(recipe_controller):
    recipe_controller.get_recipe_readiness = MagicMock(return_value=None)
    recipe = recipe_controller.get_recipe(Diet.VEGAN, True)
    assert recipe is None

@pytest.mark.unit
def test_get_recipe_best_multiple(recipe_controller):
    recipe_controller.get_recipe_readiness = MagicMock(side_effect=lambda recipe, items, diet: 1.0)
    recipes = [recipe_controller.get_recipe(Diet.VEGAN, True) for _ in range(5)]
    assert all(recipe == "Whole Grain Bread" for recipe in recipes)

@pytest.mark.unit
def test_get_recipe_random_multiple(recipe_controller):
    recipe_controller.get_recipe_readiness = MagicMock(side_effect=lambda recipe, items, diet: 1.0)
    recipes = [recipe_controller.get_recipe(Diet.VEGAN, False) for _ in range(5)]
    assert all(recipe == "Whole Grain Bread" for recipe in recipes)
