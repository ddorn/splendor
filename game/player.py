from collections import namedtuple

from game.coins import Coins


PlayerTuple = namedtuple("PlayerTuple", ["points", "coins", "production"])


class Player:
    def __init__(self):
        self.points = 0
        self.coins = Coins()
        self.production = Coins()

    def as_tuple(self):
        return PlayerTuple(self.points, self.coins, self.production)
