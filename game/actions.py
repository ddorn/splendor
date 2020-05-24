from collections import Counter

from data import *
from .coins import Coins


__all__ = ["TakeAction", "ReserveAction", "BuyAction"]


class TakeAction(tuple):
    def __new__(cls, *coins):

        assert len(coins) <= 3, "Cannot take more than 3 coins."
        assert len(coins) == 2 or len(set(coins)) == len(
            coins
        ), "Can not take two coins of the same color."
        assert set(coins).issubset(COINS), f"Not all coins have coins values {coins}."

        return tuple.__new__(cls, coins)

    def as_coins(self):
        return Coins.from_iter(self)

    def __repr__(self):
        return f"TAKE {' '.join(map(str, self))}"


class BuyAction:
    def __init__(self, card_id):
        assert card_id in ("I", "II", "III") or card_id in range(len(CARDS))
        self.card_id = card_id

    def __repr__(self):
        return f"BUY {self.card_id}"


class ReserveAction:
    def __init__(self, card_id):
        self.card_id = card_id

    def __repr__(self):
        return f"RESERVE {self.card_id}"
