from splendor.data import *
from splendor import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_noble_qte():
    assert len(NOBLES) == 10


def test_cards_qte():
    assert len(CARDS) == 90


def test_constants():
    assert START_COINS == {2: 4, 3: 5, 4: 7}
    assert RED == 0
    assert GREEN == 1
    assert BLUE == 2
    assert BLACK == 3
    assert WHITE == 4
    assert YELLOW == 5
    assert STAGE == 6
    assert PRODUCTION == 7
    assert VICTORY_POINTS == 8

    assert POINTS_FOR_WIN == 15
