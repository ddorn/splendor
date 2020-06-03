from splendor.data import *
from splendor import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_noble_qte():
    assert len(NOBLES) == 10


def test_cards_qte():
    assert len(CARDS) == 91
    assert CARDS_NB == 90
    assert CARDS[-1] is UNKNOWN_CARD

    for c in CARDS:
        assert CARDS[c.id] is c

    assert UNKNOWN_CARD.id == -1
    assert UNKNOWN == UNKNOWN_CARD.id


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
    assert STAGES == ("I", "II", "III")
