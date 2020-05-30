import sys
from time import time
from operator import itemgetter

from splendor.data import *
from splendor.game import *
from splendor.game.errors import SplendorException
from splendor.game.game import get
from splendor.interfaces.base import BaseClient
from splendor.interfaces.tui.utils import fmt, print
from tqdm import tqdm


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
                if card is not UNKNOWN_CARD and total.can_buy(card):
                    yield BuyAction(card.id)

        # Buy a reserved card.
        for card in player.reserved:
            if card is not UNKNOWN_CARD and total.can_buy(card):
                yield BuyAction(card.id)

        if len(player.reserved) < MAX_RESERVED:
            # Reserve a hidden card.
            for stage in STAGES:
                yield ReserveAction(stage)

            # Reserve a visible card.
            for stage in state.revealed_cards():
                for card in stage:
                    if card is not UNKNOWN_CARD:
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

        score = 0
        player = state.players[state.current_player_id]

        if player.points >= POINTS_FOR_WIN:
            score += 100 * (player.points - POINTS_FOR_WIN + 2)

        # One  point per card that counts for a noble.
        score += sum(player.production.min(n).total() for n in state.nobles)

        # One half point per coin that counts for a card
        # score += 0.5 * sum(player.coins.min(c[:YELLOW]).total() for age in state.deck for c in age[:4])

        score += 12 * player.production.total()
        score += player.coins.total() + player.coins.yellow * 2
        score += 12 * player.points
        return score

    def play(self, state: BaseGame):

        start = time()
        count = [0]
        MAX_DEPTH = 4
        def explore(state, depth=0):
            if depth == MAX_DEPTH:
                count[0] += 1
                yield (self.score(state), )
                return

            moves = []
            for m in self.legal_moves(state):
                new = self.apply(m, state)
                score = self.score(new)
                moves.append((m, new, score))

            moves.sort(key=itemgetter(2), reverse=True)
            to_delete = len(moves) // (depth + 2.5)
            del moves[int(to_delete):]

            it = tqdm(moves) if depth is 0 else moves
            for m, state, score in it:
                for *mvs, r in explore(state, depth+1):
                    yield (m, *mvs, score + r * 0.7)

        actions = sorted(explore(state), key=itemgetter(-1), reverse=True)
        action = actions[0]

        # print(*actions[:10], sep="\n")

        print()
        print("explored:", count[0], "duration:", round(time() - start, 2))
        print(action, bold=True)

        return action[0]


    def error(self, error: SplendorException):
        print(error, file=sys.stderr)