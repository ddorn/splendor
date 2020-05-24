from dataclasses import dataclass

from data import COINS_TO_NAMES


@dataclass(frozen=True)
class Coins:
    red: int = 0
    green: int = 0
    blue: int = 0
    black: int = 0
    white: int = 0
    yellow: int = 0

    def __iter__(self):
        yield from self.__dict__.values()

    def __getitem__(self, item):
        return getattr(self, COINS_TO_NAMES[item])

    def issubset(self, other: "Coins"):
        return all(a <= b for a, b in zip(self, other))

    def total(self):
        return sum(self)

    def __add__(self, other):
        return Coins(*[a + b for a, b in zip(self, other)])

    def __sub__(self, other):
        return Coins(*[a - b for a, b in zip(self, other)])
