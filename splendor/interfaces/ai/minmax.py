import sys

from splendor.data import *
from splendor.game import *
from splendor.game.errors import SplendorException
from splendor.interfaces.runner import BaseClient


class MinMaxAi(BaseClient):

    def legal_moves(self, state: BaseGame):
        """Generate all valid action for a given state"""

        player = state.players[state.current_player_id]
        can_take = MAX_COINS_PER_PLAYER - player.coins.total()
        bank: Coins = state.bank

        # Generate TakeActions
        yield TakeAction()

        # take two coins of the same color
        if can_take >= 2:
            for i, v in enumerate(bank[:YELLOW]):
                if v >= MIN_COINS_FOR_TAKE_TWO_SAME:
                    yield TakeAction(i, i)

        # Take up to 3 different coins.
        for combination in self.generate_diff_coins(bank, min(3, can_take)):
            yield TakeAction(*combination)

        # Buy a visible card.
        total: Coins = player.coins + player.production
        for stage in state.revealed_cards():
            for card in stage:
                if total.can_buy(card):
                    yield BuyAction(card.id)

        # Buy a reserved card.
        for card in player.reserved:
            if total.can_buy(card):
                yield BuyAction(card.id)

        if len(player.reserved) < MAX_RESERVED:
            # Reserve a hidden card.
            # for stage in STAGES:
            #     yield ReserveAction(stage)

            # Reserve a visible card.
            for stage in state.revealed_cards():
                for card in stage:
                    yield ReserveAction(card.id)

    def generate_diff_coins(self, bank, nb=3, start=0):
        """
        Generate combinations of different coins that can be taken from the bank.

        nb: maximum number of different coins
        start: don't take coins with an id smaller than that
        """

        if nb < 1:
            return

        for c in range(start, YELLOW):
            if bank[c]:
                yield c,
                for others in self.generate_diff_coins(bank, nb-1, c+1):
                    yield (c, *others)

    def apply(self, action: Action, state: BaseGame) -> BaseGame:
        """
        Apply the action on the state and return the new state.

        The action should be valid, no checks are made for efficiency.
        """

        state = state.copy()
        state.action(state.current_player, action)

        return state

    def score(self, state: BaseGame) -> float:
        """
        Return a score for a given state.

        Higher value means better for the current player.
        """

        player = state.players[state.current_player_id]

        return 3 * player.production.total() + player.coins.total() + 5 * player.points

    def play(self, state: BaseGame):
        best_score = -1
        best_action = TakeAction()
        for action in self.legal_moves(state):
            new_state = self.apply(action, state)
            score = self.score(new_state)

            if score > best_score:
                best_score = score
                best_action = action
        return best_action

    def error(self, error: SplendorException):
        print(error, file=sys.stderr)