import sys
from collections import namedtuple
from random import shuffle

from data import *
from game import TakeAction, BuyAction, ReserveAction
from game.coins import Coins
from game.player import Player
from game.errors import *


PublicState = namedtuple("PublicState", ["cards", "coins", "players"])


class Game:
    def __init__(self, *clients):
        self.clients = clients
        self.players = [Player() for _ in clients]
        self.deck = [[c for c in CARDS if c[STAGE] == age] for age in (1, 2, 3)]

        shuffle(NOBLES)
        self.nobles = NOBLES[: len(clients) + 1]
        self.bank = Coins()

    def ended(self):
        """Whether the game is over."""
        return any(p.points >= POINTS_FOR_WIN for p in self.players)

    def run(self):
        while not self.ended():
            for player, client in zip(self.players, self.clients):
                while True:
                    try:
                        self.action(player, client.play(self.public_state))
                    except Exception as e:
                        print(e, file=sys.stderr)
                    else:
                        break

    def action(self, player, action):
        """
        Perform an action as a player.

        This does no check to see whether a it is this player's turn.
        """

        if isinstance(action, TakeAction):
            if len(action) > 3:
                raise TakeCoinsException("Cannot take more than 3 coins.", action)
            if len(action) != len(set(action)) and len(action) != 2:
                raise TakeCoinsException("Can only take two coins alone.", action)
            if YELLOW in TakeAction:
                raise TakeCoinsException("Cannot take yellow coin.", action)
            if not COINS.issuperset(TakeAction):
                raise TakeCoinsException("Not all coins are valid numbers.", action)

            wanted = action.as_coins()
            if not wanted.issubset(self.bank):
                raise NotEnoughCoins(self.bank, wanted)

            two_same = len(action) == 2 and action[0] == action[1]

            if two_same:
                color = action[0]

            else:
                ...

            self._take_action(player, action)

        elif isinstance(action, BuyAction):
            ...

        elif isinstance(action, ReserveAction):
            ...

    def _take_action(self, player, take: TakeAction):
        """Perform a TakeAction without checking anything."""

    @property
    def public_state(self):
        return PublicState(
            [self.deck[age][:4] for age in range(3)],
            self.bank,
            [p.as_tuple() for p in self.players],
        )
