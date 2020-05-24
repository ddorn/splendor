from collections import Counter
from dataclasses import dataclass

from data import COINS_TO_NAMES, YELLOW


@dataclass(frozen=True)
class Coins:
    red: int = 0
    green: int = 0
    blue: int = 0
    black: int = 0
    white: int = 0
    yellow: int = 0

    @classmethod
    def from_iter(cls, iterable):
        """Construct a Coins from an iterable of coin IDs."""
        return Coins(
            **{COINS_TO_NAMES[color]: nb for color, nb in Counter(iterable).items()}
        )

    def as_iter(self):
        for i, v in enumerate(self):
            for _ in range(v):
                yield i

    def __repr__(self):
        return " ".join(f"{v}{'RGBKWY'[i]}" for i, v in enumerate(self) if v) or "0c"

    def __iter__(self):
        yield from self.__dict__.values()

    def __getitem__(self, item):
        if isinstance(item, slice):
            # We could use this method all the time but it is slower
            return tuple(self)[item]

        return getattr(self, COINS_TO_NAMES[item])

    def __add__(self, other):
        return Coins(*[a + b for a, b in zip(self, other)])

    def __sub__(self, other):
        return Coins(*[a - b for a, b in zip(self, other)])

    def __mul__(self, other):
        return Coins(*[a * other for a in self])

    __rmul__ = __mul__

    def issubset(self, other: "Coins", yellow_as_joker=False):
        """
        Whether there is more coins of each color in other.

        If yellow_as_joker is True, the yellow coins of other can replace any
        color of self and the yellow of self are ignored.
        """

        if yellow_as_joker:
            missing = sum(max(a - b, 0) for a, b in zip(self[:YELLOW], other[:YELLOW]))
            return missing <= other.yellow
        return all(a <= b for a, b in zip(self, other))

    def total(self):
        return sum(self)

    def clamp(self):
        """A Coins with all the value below 0 clamped to 0."""
        return Coins(*(v if v >= 0 else 0 for v in self))


red_coin = Coins(red=1)
green_coin = Coins(green=1)
blue_coin = Coins(blue=1)
black_coin = Coins(black=1)
white_coin = Coins(white=1)
yellow_coin = Coins(yellow=1)

one_coins = (red_coin, green_coin, blue_coin, black_coin, white_coin, yellow_coin)
