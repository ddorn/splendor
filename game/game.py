import sys
from operator import attrgetter
from random import shuffle

from data import *
from game import TakeAction, BuyAction, ReserveAction
from game.coins import Coins, one_coins
from game.player import Player
from game.errors import *


def get(objs, **attrs):
    getter = attrgetter(*attrs)
    # getter dosen't return a tuple when only one attr is passed.
    value = tuple(attrs.values()) if len(attrs) > 1 else attrs.popitem()[1]

    for obj in objs:
        if getter(obj) == value:
            return obj


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
        reserved = get(player.reserved, id=buy.card_id)
        print(reserved)
        from pprint import pprint

        pprint(player.reserved)

        if reserved:
            card = reserved
        else:
            card = self.get_visible_card(buy.card_id)

        if not card:
            raise NoSuchCard(buy.card_id)

        # check if we can buy it
        cost = Coins(*card[:YELLOW], 0)
        if not cost.issubset(player.coins + player.production):
            raise NotEnoughCoins(player.coins + player.production, cost)

        # pay
        coin_cost = (cost - player.production).clamp()
        missing = (coin_cost - player.coins).clamp()
        coin_cost = coin_cost - missing + Coins(yellow=missing.total())
        self.bank += coin_cost
        player.coins -= coin_cost

        # construct it
        player.points += card.points
        player.production += one_coins[card.production]

        if reserved:
            player.reserved.remove(card)
        else:
            self.deck[STAGES.find(card.stage)].remove(card)

        # check nobles
        noble = self.check_nobles(player)
        if noble:
            self.nobles.remove(noble)
            player.points += POINTS_PER_NOBLE

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

    def check_nobles(self, player):
        for noble in self.nobles:
            if Coins(*noble).issubset(player.production):
                return noble

    @property
    def public_state(self):
        return PublicState(
            tuple(tuple(self.deck[age][:4]) for age in range(3)),
            self.bank,
            tuple(p.as_tuple() for p in self.players),
        )
