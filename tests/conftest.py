import sys
from pathlib import Path
from typing import Callable
from unittest.mock import Mock

# Добавляем корневую папку проекта в sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from praktikum.burger import Burger
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient


@pytest.fixture
def burger() -> Burger:
    """Создаёт пустой бургер без булки и ингредиентов."""
    return Burger()


@pytest.fixture
def mock_bun() -> Mock:
    """Мок-булка с фиксированными значениями: имя 'test bun', цена 10.0."""
    bun = Mock(spec=Bun)
    bun.get_name.return_value = "test bun"
    bun.get_price.return_value = 10.0
    return bun


@pytest.fixture
def mock_ingredient() -> Mock:
    """Мок-ингредиент с фиксированными значениями: тип 'sauce', имя 'test sauce', цена 15.0."""
    ingredient = Mock(spec=Ingredient)
    ingredient.get_type.return_value = "sauce"
    ingredient.get_name.return_value = "test sauce"
    ingredient.get_price.return_value = 15.0
    return ingredient


@pytest.fixture
def ingredient_factory() -> Callable[..., Mock]:
    """
    Фабрика для создания моков Ingredient с произвольными параметрами.
    Возвращает функцию, которая принимает type, name, price и возвращает мок.
    """
    def _create_ingredient(ingredient_type: str = "sauce",
                           name: str = "custom sauce",
                           price: float = 20.0) -> Mock:
        ing = Mock(spec=Ingredient)
        ing.get_type.return_value = ingredient_type
        ing.get_name.return_value = name
        ing.get_price.return_value = price
        return ing
    return _create_ingredient


@pytest.fixture
def bun_factory() -> Callable[..., Mock]:
    """Фабрика для создания моков Bun с произвольными параметрами."""
    def _create_bun(name: str = "custom bun", price: float = 25.0) -> Mock:
        bun = Mock(spec=Bun)
        bun.get_name.return_value = name
        bun.get_price.return_value = price
        return bun
    return _create_bun


@pytest.fixture
def burger_with_three_ingredients(burger: Burger, ingredient_factory: Callable) -> Burger:
    """
    Возвращает бургер с тремя ингредиентами с именами 'first', 'second', 'third'.
    """
    ing1 = ingredient_factory(name="first")
    ing2 = ingredient_factory(name="second")
    ing3 = ingredient_factory(name="third")
    burger.add_ingredient(ing1)
    burger.add_ingredient(ing2)
    burger.add_ingredient(ing3)
    return burger