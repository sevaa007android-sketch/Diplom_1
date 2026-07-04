import pytest
from praktikum.burger import Burger


def test_burger_initial_state(burger):
    """Проверяем, что при создании бургера булка равна None, а список ингредиентов пуст."""
    assert burger.bun is None
    assert burger.ingredients == []
    
def test_set_buns(burger, mock_bun):
    """Проверяем, что метод set_buns правильно устанавливает булку."""
    burger.set_buns(mock_bun)
    assert burger.bun == mock_bun
    
@pytest.mark.parametrize("count", [1, 3])
def test_add_ingredient(burger, mock_ingredient, count):
    """Проверяем добавление одного и нескольких ингредиентов."""
    for _ in range(count):
        burger.add_ingredient(mock_ingredient)
    assert len(burger.ingredients) == count
    for ing in burger.ingredients:
        assert ing == mock_ingredient