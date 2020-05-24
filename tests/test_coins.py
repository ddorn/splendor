from pytest import raises, mark

from game.coins import Coins


def test_coins_immutable():
    coins = Coins()

    with raises(AttributeError):
        coins.red = 2

    with raises(AttributeError):
        coins.yellow = 9


@mark.parametrize(
    "a,b",
    [
        (Coins(), Coins(0, 0, 0, 0, 0, 0)),
        (Coins(1, 2), Coins(1, 2, 0)),
        (Coins(red=4, white=2), Coins(4, 0, 0, 0, 2)),
        (Coins(yellow=9), Coins(0, 0, 0, 0, 0, 9)),
        (Coins(1, 2, 3, 4, 5), Coins(red=1, green=2, blue=3, black=4, white=5)),
    ],
)
def test_coins_equality(a, b):
    assert a == b


@mark.parametrize(
    "a,b,expected",
    [
        (Coins(3), Coins(6), True),
        (Coins(1, 2, 3, 4, 5, 6), Coins(2, 3, 4, 5, 6, 7), True),
        (Coins(yellow=1), Coins(), False),
        (Coins(1, 2, 3, 4), Coins(0, 2, 3, 4), False),
        (Coins(2, 2, 2), Coins(2, 1, 2), False),
    ],
)
def test_coins_issubset(a: Coins, b: Coins, expected):
    assert a.issubset(b) == expected
    assert b.issubset(a) != expected


def test_coins_issubset_empty():
    empty = Coins()
    assert empty.issubset(empty)


def test_coins_iter():
    c = Coins(1, 2, 3, 4, 5, 6)
    for i, v in enumerate(c):
        assert v == i + 1
        assert c[i] == i + 1

    assert tuple(c) == (1, 2, 3, 4, 5, 6)


@mark.parametrize(
    "coins,expected",
    [
        (Coins(), 0),
        (Coins(yellow=2), 2),
        (Coins(2, 4, black=4), 10),
        (Coins(green=23, white=2), 25),
    ],
)
def test_coins_total(coins, expected):
    assert coins.total() == expected
