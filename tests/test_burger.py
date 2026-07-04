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

@pytest.mark.parametrize("index, expected_list", [
    (0, ["second", "third"]),   # удаляем первый
    (1, ["first", "third"]),    # удаляем средний
    (2, ["first", "second"]),   # удаляем последний
])
def test_remove_ingredient_valid(burger, ingredient_factory, index, expected_list):
    """Проверяем удаление ингредиента по валидному индексу."""
    # Создаём три ингредиента с разными именами
    ing1 = ingredient_factory(name="first")
    ing2 = ingredient_factory(name="second")
    ing3 = ingredient_factory(name="third")
    
    burger.add_ingredient(ing1)
    burger.add_ingredient(ing2)
    burger.add_ingredient(ing3)
    
    # Удаляем по индексу
    burger.remove_ingredient(index)
    
    # Проверяем, что остались только нужные ингредиенты (сравниваем имена)
    remaining_names = [ing.get_name() for ing in burger.ingredients]
    assert remaining_names == expected_list


def test_remove_ingredient_invalid_index(burger, ingredient_factory):
    """Проверяем, что при невалидном индексе возникает IndexError."""
    burger.add_ingredient(ingredient_factory(name="only_one"))
    
    with pytest.raises(IndexError):
        burger.remove_ingredient(10)   # индекс вне диапазона