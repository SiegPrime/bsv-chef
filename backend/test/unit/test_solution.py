import pytest
from unittest.mock import MagicMock
from src.controllers.recipecontroller import RecipeController
from src.util.dao import DAO
from src.static.diets import Diet

@pytest.fixture
def controller():
    dao = DAO()
    controller = RecipeController(items_dao=dao)

    controller.get_all = lambda: [
        {"name": "item1", "quantity": -1},
        {"name": "item2", "quantity": 0},
        {"name": "item3", "quantity": 1},
        {"name": "item4", "quantity": 5}
    ]

    return controller

@pytest.mark.unit
def test_1(self):
    expected_result = {
        "item1": -1,
        "item2": 0,
        "item3": 1,
        "item4": 5
    }
    assert self.controller.get_available_items(minimum_quantity=-2) == expected_result

@pytest.mark.unit
def test_2(self):
    expected_result = {
        "item1": -1,
        "item2": 0
    }
    assert self.controller.get_available_items(minimum_quantity=-1) == expected_result

@pytest.mark.unit
def test_3(self):
    expected_result = {
        "item2": 0,
        "item3": 1,
        "item4": 5
    }
    assert self.controller.get_available_items(minimum_quantity=0) == expected_result

@pytest.mark.unit
def test_4(self):
    expected_result = {
        "item3": 1,
        "item4": 5
    }
    assert self.controller.get_available_items(minimum_quantity=1) == expected_result
