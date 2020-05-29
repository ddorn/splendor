from splendor.game.coins import Coins


class Player:
    def __init__(self):
        self.points = 0
        self.coins = Coins()
        self.production = Coins()
        self.reserved = []

    def __repr__(self):
        return f"<Player(points={self.points}, coins={self.coins}, production={self.production}, reserved={self.reserved})>"

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.points == other.points and self.coins == other.coins and self.production == other.production and self.reserved == other.reserved

    def copy(self):
        p = Player()
        p.points = self.points
        p.coins = self.coins
        p.production = self.production
        p.reserved = list(self.reserved)

        return p
