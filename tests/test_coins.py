from pytest import raises, mark

from splendor.game.coins import Coins


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


@mark.parametrize(
    "a,b,expected",
    [
        (Coins(1), Coins(yellow=1), True),
        (Coins(2), Coins(1, yellow=1), True),
        (Coins(blue=3), Coins(blue=1, yellow=1), False),
        (Coins(1, 2, 3), Coins(0, 2, 1, yellow=3), True),
        (Coins(1, 2, 3), Coins(0, 2, 1, yellow=8), True),
        (Coins(2, 2, 2), Coins(2, 0, 2, yellow=1), False),
    ],
)
def test_coins_issubset_yellow(a, b, expected):
    assert a.issubset(b, True) == expected


def test_coins_issubset_empty():
    empty = Coins()
    assert empty.issubset(empty)


@mark.parametrize(
    'card,coins,expected',
    [
        ((3, 1, 1,), Coins(2, 0, 3, 1, 1, 2), True),
        ((0, 1, 1, 1,), Coins(yellow=3), True),
        ((0, 1, 1, 1,), Coins(yellow=2), False),
        ((0, 1, 1, 1,), Coins(1, yellow=2), False),
    ]
)
def test_coins_can_buy(card, coins, expected):
    assert coins.can_buy(card) == expected

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


@mark.parametrize(
    "a,b,c",
    [
        (Coins(1), Coins(), Coins(1)),
        (Coins(yellow=3), Coins(yellow=2), Coins(yellow=5)),
        (Coins(1, 2), Coins(3, 4), Coins(4, 6)),
        (Coins(black=1, blue=2), Coins(1, 2, 3, yellow=1), Coins(1, 2, 5, 1, 0, 1)),
    ],
)
def test_coins_sum(a, b, c):
    assert a + b == c


@mark.parametrize(
    "a,b,c",
    [
        (Coins(1), Coins(), Coins(1)),
        (Coins(yellow=3), Coins(yellow=2), Coins(yellow=1)),
        (Coins(1, 2), Coins(3, 4), Coins(-2, -2)),
        (Coins(4, 4, 4, 4, 4, 4), Coins(1, 2, 3, yellow=1), Coins(3, 2, 1, 4, 4, 3)),
    ],
)
def test_coins_sub(a, b, c):
    assert a - b == c
