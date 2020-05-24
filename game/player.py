from collections import namedtuple

from game.coins import Coins


PlayerTuple = namedtuple("PlayerTuple", ["points", "coins", "production", "reserved"])


class Player:
    def __init__(self):
        self.points = 0
        self.coins = Coins()
        self.production = Coins()
        self.reserved = []

    def as_tuple(self):
        return PlayerTuple(
            self.points, self.coins, self.production, tuple(self.reserved)
        )

    def __repr__(self):
        return f"<Player(points={self.points}, coins={self.coins}, production={self.production}, reserved={self.reserved})>"
