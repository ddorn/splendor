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
        assert len(clients) in range(2, 5)

        self.clients = clients
        self.players = [Player() for _ in clients]
        self.deck = [[c for c in CARDS if c.stage == stage] for stage in STAGES]

        nobles = list(NOBLES)
        shuffle(nobles)
        self.nobles = nobles[: len(clients) + 1]

        sc = START_COINS[len(clients)]
        self.bank = Coins(sc, sc, sc, sc, sc, 5)

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

        {
            TakeAction: self._take_action,
            BuyAction: self._buy_action,
            ReserveAction: self._reserve_action,
        }[action.__class__](player, action)

    def _take_action(self, player, take: TakeAction):
        if len(take) > 3:
            raise TakeCoinsException("Cannot take more than 3 coins.", take)
        if len(take) != len(set(take)) and len(take) != 2:
            raise TakeCoinsException("Can only take two coins alone.", take)
        if YELLOW in take:
            raise TakeCoinsException("Cannot take yellow coin.", take)
        if not COINS.issuperset(take):
            raise TakeCoinsException("Not all coins are valid numbers.", take)

        wanted = take.as_coins()

        total = wanted.total() + player.coins.total()
        if total > MAX_COINS_PER_PLAYER:
            raise TooManyCoins(wanted.total(), total)

        if not wanted.issubset(self.bank):
            raise NotEnoughCoins(self.bank, wanted)

        two_same = len(take) == 2 and take[0] == take[1]

        if two_same:
            color = take[0]
            if self.bank[color] < MIN_COINS_FOR_TAKE_TWO_SAME:
                raise NotEnoughCoins(self.bank, wanted)

        self.bank -= wanted
        player.coins += wanted

    def _buy_action(self, player: Player, buy: BuyAction):
        # Get the card
        ...

    def _reserve_action(self, player: Player, reserve: ReserveAction):

        if len(player.reserved) >= MAX_RESERVED:
            raise ReserveFull()

        # Get the card
        card: Card
        if reserve.card_id in STAGES:
            stage = STAGES.index(reserve.card_id)

            if len(self.deck[stage]) <= VISIBLE_CARDS:
                raise EmptyDeck(reserve.card_id)

            card = self.deck[stage][VISIBLE_CARDS]
        else:
            card = self.get_visible_card(reserve.card_id)
            if not card:
                raise NoSuchCard(reserve.card_id)

            stage = STAGES.index(card.stage)

        self.deck[stage].remove(card)
        player.reserved.append(card)

        if player.coins.total() < MAX_COINS_PER_PLAYER and self.bank.yellow > 0:
            player.coins += Coins(yellow=1)
            self.bank -= Coins(yellow=1)

    def get_visible_card(self, card_id):
        candidates = [
            c for stage in self.deck for c in stage[:VISIBLE_CARDS] if c.id == card_id
        ]

        assert len(candidates) <= 1, "There are two cards with the same id ???"

        return candidates[0] if candidates else None

    @property
    def public_state(self):
        return PublicState(
            tuple(tuple(self.deck[age][:4]) for age in range(3)),
            self.bank,
            tuple(p.as_tuple() for p in self.players),
        )
