import sys
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unittest.mock import Mock
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient


@pytest.fixture
def burger():
    """Создаёт пустой бургер."""
    return Burger()


@pytest.fixture
def mock_bun():
    """Мок-булка с фиксированными значениями."""
    bun = Mock(spec=Bun)
    bun.get_name.return_value = "test bun"
    bun.get_price.return_value = 10.0
    return bun


@pytest.fixture
def mock_ingredient():
    """Мок-ингредиент с фиксированными значениями."""
    ingredient = Mock(spec=Ingredient)
    ingredient.get_type.return_value = "sauce"
    ingredient.get_name.return_value = "test sauce"
    ingredient.get_price.return_value = 15.0
    return ingredient


@pytest.fixture
def burger_with_bun_and_ingredient(burger, mock_bun, mock_ingredient):
    """Бургер с булкой и одним ингредиентом."""
    burger.set_buns(mock_bun)
    burger.add_ingredient(mock_ingredient)
    return burger


@pytest.fixture
def ingredient_factory():
    """Фабрика моков ингредиентов."""
    def _create_ingredient(ingredient_type="sauce", name="custom sauce", price=20.0):
        ing = Mock(spec=Ingredient)
        ing.get_type.return_value = ingredient_type
        ing.get_name.return_value = name
        ing.get_price.return_value = price
        return ing
    return _create_ingredient


@pytest.fixture
def bun_factory():
    """Фабрика моков булок."""
    def _create_bun(name="custom bun", price=25.0):
        bun = Mock(spec=Bun)
        bun.get_name.return_value = name
        bun.get_price.return_value = price
        return bun
    return _create_bun