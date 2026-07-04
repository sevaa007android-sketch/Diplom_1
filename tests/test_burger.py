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

       
@pytest.mark.parametrize("index, new_index, expected_order", [
    (0, 1, ["second", "first", "third"]),      # перемещаем первый на второе место
    (1, 0, ["second", "first", "third"]),      # перемещаем второй на первое место
    (2, 0, ["third", "first", "second"]),      # перемещаем последний на первое место
    (0, 0, ["first", "second", "third"]),      # перемещаем на ту же позицию (без изменений)
])
def test_move_ingredient_valid(burger, ingredient_factory, index, new_index, expected_order):
    """Проверяем корректное перемещение ингредиента."""
    # Создаём три ингредиента с разными именами
    ing1 = ingredient_factory(name="first")
    ing2 = ingredient_factory(name="second")
    ing3 = ingredient_factory(name="third")
    
    burger.add_ingredient(ing1)
    burger.add_ingredient(ing2)
    burger.add_ingredient(ing3)
    
    # Перемещаем
    burger.move_ingredient(index, new_index)
    
    # Проверяем порядок имён
    order = [ing.get_name() for ing in burger.ingredients]
    assert order == expected_order


def test_move_ingredient_invalid_index(burger, ingredient_factory):
    """Проверяем, что при невалидном index возникает IndexError."""
    burger.add_ingredient(ingredient_factory(name="only_one"))
    
    with pytest.raises(IndexError):
        burger.move_ingredient(10, 0)   # index вне диапазона 
        

@pytest.mark.parametrize("bun_price, ingredient_prices, expected", [
    (10, [15, 20], 55),           # 10*2 + 15 + 20 = 55
    (5, [10, 5], 25),             # 5*2 + 10 + 5 = 25
    (0, [], 0),                   # только булка бесплатная
    (3.5, [1.1, 2.2], 10.3),      # дробные цены
    (100, [50, 60, 70], 380),     # несколько ингредиентов
])
def test_get_price(burger, bun_factory, ingredient_factory, bun_price, ingredient_prices, expected):
    """Проверяем расчёт цены бургера."""
    # Создаём булку с заданной ценой
    bun = bun_factory(price=bun_price)
    burger.set_buns(bun)

    # Добавляем ингредиенты с ценами
    for price in ingredient_prices:
        ing = ingredient_factory(price=price)
        burger.add_ingredient(ing)

    # Проверяем итоговую цену (используем approx для float)
    assert burger.get_price() == pytest.approx(expected)