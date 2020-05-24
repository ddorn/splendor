import pytest

from data import *
from game import Coins
from game.actions import *


def test_action_repr():
    take = TakeAction(RED, GREEN, BLUE)
    assert repr(take) == "TAKE 0 1 2"

    take = TakeAction(WHITE, WHITE)
    assert repr(take) == "TAKE 4 4"

    buy = BuyAction(7)
    assert repr(buy) == "BUY 7"

    reserve = ReserveAction(12)
    assert repr(reserve) == "RESERVE 12"


@pytest.mark.parametrize(
    "action,coins",
    [
        (TakeAction(RED, RED), Coins(red=2)),
        (TakeAction(RED, WHITE, YELLOW), Coins(red=1, white=1, yellow=1)),
        (TakeAction(BLACK, BLUE), Coins(blue=1, black=1)),
        (TakeAction(GREEN), Coins(green=1)),
        (TakeAction(), Coins()),
    ],
)
def test_take_action_as_coins(action: TakeAction, coins: Coins):
    assert action.as_coins() == coins
