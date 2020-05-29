from dataclasses import dataclass
from operator import attrgetter
from random import shuffle
from typing import List, Tuple

from splendor.data import *
from splendor.game import TakeAction, BuyAction, ReserveAction
from splendor.game.coins import Coins, one_coins
from splendor.game.player import Player
from splendor.game.errors import *


def get(objs, **attrs):
    getter = attrgetter(*attrs)
    # getter dosen't return a tuple when only one attr is passed.
    value = tuple(attrs.values()) if len(attrs) > 1 else attrs.popitem()[1]

    for obj in objs:
        if getter(obj) == value:
            return obj


@dataclass
class BaseGame:
    """Game class that implements the logic but with no checks."""

    current_player_id: int
    deck: List[List[Card]]
    bank: Coins
    players: List[Player]
    nobles: List[Tuple[int, int, int, int, int, int]]

    @property
    def current_player(self):
        return self.players[self.current_player_id]

    def copy(self):
        return BaseGame(self.current_player_id, [stage[:] for stage in self.deck], self.bank, [p.copy() for p in self.players],
                        self.nobles[:])

    def ended(self):
        """Whether the game is over."""
        return self.current_player_id == 0 and any(
            p.points >= POINTS_FOR_WIN for p in self.players
        )

    def action(self, player, action):
        """
        Perform an action as a player.

        This does no check to see whether it is this player's turn
        nor whether the game has ended.
        """

        {
            TakeAction: self._take_action,
            BuyAction: self._buy_action,
            ReserveAction: self._reserve_action,
        }[action.__class__](player, action)

    def _take_action(self, player, take: TakeAction):
        """Perform a TakeAction with no checks."""
        wanted = take.as_coins()
        self.bank -= wanted
        player.coins += wanted

    def _buy_card(self, player, buy: BuyAction):
        """Return the card refered by the action and whether it is a reserved card.

        Return (None, False) if the card isn't found
        """

        reserved = get(player.reserved, id=buy.card_id)

        if reserved:
            return reserved, True
        else:
            card = self.get_visible_card(buy.card_id)
            if card:
                return card, False
        return None, False

    def _buy_action(self, player: Player, buy: BuyAction):
        # Get the card
        card, reserved = self._buy_card(player, buy)

        cost = Coins(*card[:YELLOW], 0)

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
            self.deck[STAGES.index(card.stage)].remove(card)

        # check nobles
        noble = self.check_nobles(player)
        if noble:
            self.nobles.remove(noble)
            player.points += POINTS_PER_NOBLE

    def _reserve_action(self, player: Player, reserve: ReserveAction):

        # Get the card
        card: Card
        if reserve.card_id in STAGES:
            stage = STAGES.index(reserve.card_id)
            card = self.deck[stage][VISIBLE_CARDS]
        else:
            card = self.get_visible_card(reserve.card_id)
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

    def revealed_cards(self):
        return [self.deck[age][:VISIBLE_CARDS] for age in range(3)]


class Game(BaseGame):
    def __init__(self, nb_players=4):
        assert nb_players in range(2, 5), nb_players

        players = [Player() for _ in range(nb_players)]

        deck = [[c for c in CARDS if c.stage == stage] for stage in STAGES]
        for stage in deck:
            shuffle(stage)

        nobles = list(NOBLES)
        shuffle(nobles)
        nobles = nobles[: nb_players + 1]

        sc = START_COINS[nb_players]
        bank = Coins(sc, sc, sc, sc, sc, 5)

        super().__init__(0, deck, bank, players, nobles)

    def play(self, action):
        """Perform an action for the current player."""

        if self.ended():
            raise GameEnded()

        player = self.players[self.current_player_id]
        self.action(player, action)

        self.current_player_id += 1
        self.current_player_id %= len(self.players)

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
            if self.bank[take[0]] < MIN_COINS_FOR_TAKE_TWO_SAME:
                raise NotEnoughCoins(self.bank, wanted)

        super()._take_action(player, take)

    def _buy_action(self, player: Player, buy: BuyAction):
        card, _ = self._buy_card(player, buy)

        if not card:
            raise NoSuchCard(buy.card_id)

        # check if we can buy it
        cost = Coins(*card[:YELLOW], 0)
        if not cost.issubset(player.coins + player.production, yellow_as_joker=True):
            raise NotEnoughCoins(player.coins + player.production, cost)

        super(Game, self)._buy_action(player, buy)

    def _reserve_action(self, player: Player, reserve: ReserveAction):

        if len(player.reserved) >= MAX_RESERVED:
            raise ReserveFull()

        # Get the card
        card: Card
        if reserve.card_id in STAGES:
            stage = STAGES.index(reserve.card_id)
            if len(self.deck[stage]) <= VISIBLE_CARDS:
                raise EmptyDeck(reserve.card_id)
        else:
            card = self.get_visible_card(reserve.card_id)
            if not card:
                raise NoSuchCard(reserve.card_id)

        super(Game, self)._reserve_action(player, reserve)

    @property
    def public_state(self) -> BaseGame:
        return BaseGame(
            self.current_player_id,
            [
                [
                    c if i < VISIBLE_CARDS else UNKNOWN_CARD
                    for i, c in enumerate(stage)
                ] for stage in self.deck
            ],
            self.bank,
            [p.copy() for p in self.players],
            self.nobles[:],
        )
