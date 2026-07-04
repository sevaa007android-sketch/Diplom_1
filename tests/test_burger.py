import pytest
from unittest.mock import Mock
from praktikum.burger import Burger


# ---------- Тесты для __init__ ----------
def test_burger_initial_state(burger: Burger) -> None:
    """Проверяем, что при создании бургера булка равна None, а список ингредиентов пуст."""
    assert burger.bun is None
    assert burger.ingredients == []


# ---------- Тесты для set_buns ----------
def test_set_buns(burger: Burger, mock_bun: Mock) -> None:
    """Проверяем, что метод set_buns правильно устанавливает булку."""
    burger.set_buns(mock_bun)
    assert burger.bun == mock_bun


# ---------- Тесты для add_ingredient ----------
@pytest.mark.parametrize("count", [1, 3])
def test_add_ingredient(burger: Burger, mock_ingredient: Mock, count: int) -> None:
    """Проверяем добавление одного и нескольких ингредиентов."""
    for _ in range(count):
        burger.add_ingredient(mock_ingredient)
    assert len(burger.ingredients) == count
    for ing in burger.ingredients:
        assert ing == mock_ingredient


# ---------- Тесты для remove_ingredient ----------
@pytest.mark.parametrize("index, expected_names", [
    (0, ["second", "third"]),
    (1, ["first", "third"]),
    (2, ["first", "second"]),
])
def test_remove_ingredient_valid(burger_with_three_ingredients: Burger, index: int, expected_names: list) -> None:
    """Проверяем удаление ингредиента по валидному индексу (первый, средний, последний)."""
    burger = burger_with_three_ingredients
    burger.remove_ingredient(index)
    remaining_names = [ing.get_name() for ing in burger.ingredients]
    assert remaining_names == expected_names


def test_remove_ingredient_invalid_index(burger: Burger, ingredient_factory) -> None:
    """Проверяем, что при невалидном индексе возникает IndexError."""
    burger.add_ingredient(ingredient_factory(name="only_one"))
    with pytest.raises(IndexError):
        burger.remove_ingredient(10)


# ---------- Тесты для move_ingredient ----------
@pytest.mark.parametrize("index, new_index, expected_names", [
    (0, 1, ["second", "first", "third"]),
    (1, 0, ["second", "first", "third"]),
    (2, 0, ["third", "first", "second"]),
    (0, 0, ["first", "second", "third"]),
])
def test_move_ingredient_valid(burger_with_three_ingredients: Burger, index: int, new_index: int, expected_names: list) -> None:
    """Проверяем корректное перемещение ингредиента (разные комбинации)."""
    burger = burger_with_three_ingredients
    burger.move_ingredient(index, new_index)
    order = [ing.get_name() for ing in burger.ingredients]
    assert order == expected_names


def test_move_ingredient_invalid_index(burger: Burger, ingredient_factory) -> None:
    """Проверяем, что при невалидном index возникает IndexError."""
    burger.add_ingredient(ingredient_factory(name="only_one"))
    with pytest.raises(IndexError):
        burger.move_ingredient(10, 0)


# ---------- Тесты для get_price ----------
@pytest.mark.parametrize("bun_price, ingredient_prices, expected", [
    (10, [15, 20], 55),
    (5, [10, 5], 25),
    (0, [], 0),
    (3.5, [1.1, 2.2], 10.3),
    (100, [50, 60, 70], 380),
])
def test_get_price(burger: Burger, bun_factory, ingredient_factory, bun_price: float, ingredient_prices: list, expected: float) -> None:
    """Проверяем расчёт цены бургера."""
    bun = bun_factory(price=bun_price)
    burger.set_buns(bun)
    for price in ingredient_prices:
        ing = ingredient_factory(price=price)
        burger.add_ingredient(ing)
    assert burger.get_price() == pytest.approx(expected)


# ---------- Тесты для get_receipt ----------
def test_get_receipt(burger: Burger, bun_factory, ingredient_factory) -> None:
    """Проверяем формирование чека с ингредиентами."""
    bun = bun_factory(name="black bun", price=100)
    ing1 = ingredient_factory(ingredient_type="sauce", name="hot sauce", price=50)
    ing2 = ingredient_factory(ingredient_type="filling", name="cutlet", price=80)

    burger.set_buns(bun)
    burger.add_ingredient(ing1)
    burger.add_ingredient(ing2)

    # Мокаем get_price, чтобы изолировать тест форматирования от логики расчёта
    burger.get_price = Mock(return_value=330.0)

    expected_receipt = (
        "(==== black bun ====)\n"
        "= sauce hot sauce =\n"
        "= filling cutlet =\n"
        "(==== black bun ====)\n"
        "\n"
        "Price: 330.0"
    )
    assert burger.get_receipt() == expected_receipt


def test_get_receipt_no_ingredients(burger: Burger, bun_factory) -> None:
    """Проверяем чек без ингредиентов."""
    bun = bun_factory(name="white bun", price=50)
    burger.set_buns(bun)
    burger.get_price = Mock(return_value=100.0)

    expected_receipt = (
        "(==== white bun ====)\n"
        "(==== white bun ====)\n"
        "\n"
        "Price: 100.0"
    )
    assert burger.get_receipt() == expected_receipt