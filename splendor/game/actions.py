from splendor.data import *
from .coins import Coins


__all__ = ["TakeAction", "ReserveAction", "BuyAction"]

from .errors import ActionParseError


class Action:
    @staticmethod
    def from_str(s: str):
        words = s.strip().split()

        if not words:
            raise ActionParseError("String is empty.")

        cls = {"TAKE": TakeAction, "BUY": BuyAction, "RESERVE": ReserveAction}.get(
            words[0].upper()
        )

        if cls is None:
            raise ActionParseError(
                f"The first word ({words[0]}) is not TAKE, BUY nor RESERVE."
            )

        if cls is TakeAction:
            # Colors can be named
            rev = {color: i for i, color in COINS_TO_NAMES.items()}
            # Or digits
            rev.update({str(i): i for i in range(YELLOW + 1)})
            args = [rev.get(a.lower()) for a in words[1:]]
            if None in args:
                c = next(w for w, a in zip(words[1:], args) if a is None)
                raise ActionParseError(f"'{c}' is not a valid color name.")
        else:
            if len(words) != 2:
                raise ActionParseError(f"Missing argument card_id.")
            try:
                args = (int(words[1]),)
            except ValueError:
                args = (words[1],)

        try:
            return cls(*args)
        except AssertionError as e:
            raise ActionParseError(e.args[0])


class TakeAction(tuple, Action):
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


class BuyAction(Action):
    def __init__(self, card_id):
        assert card_id in range(len(CARDS)), f"Invalid card id"
        self.card_id = card_id

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.card_id == other.card_id

    def __repr__(self):
        return f"BUY {self.card_id}"


class ReserveAction(Action):
    def __init__(self, card_id):
        assert card_id in ("I", "II", "III") or card_id in range(
            len(CARDS)
        ), f"Invalid card id"
        self.card_id = card_id

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.card_id == other.card_id

    def __repr__(self):
        return f"RESERVE {self.card_id}"
