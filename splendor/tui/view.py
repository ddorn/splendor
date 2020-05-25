from data import *
from game import *
from game.errors import *
from splendor.runner import BaseViewClient
from .utils import *


class TuiView(BaseViewClient):
    def show(self, game: Game):
        print("\033[2J", end="")  # clear screen
        print(f" Player: {game.player_idx} ".center(32, "="))
        print()

        print(fmt("Bank:", ul=True), self.coins_str(game.bank))
        print()

        for i, age in enumerate(game.revealed_cards()):
            print("Age", fmt(STAGES[i], bold=True), ul=True)

            for card in age:
                print(self.card_str(card), indent=2)
            print()

        for i, player in enumerate(game.players):
            print("Player", fmt(i, bold=1), ul=True)
            print(self.player_str(player), indent=2)
            print()

    def show_error(self, error: SplendorException):
        print(error.msg, fg=0xFF0000)

    @classmethod
    def card_str(cls, card: Card):
        i = fmt(card.id, it=True)
        c = cls.coins_str(Coins(*card[:YELLOW]))
        p = fmt(COINS_LETTER[card.production], fg=card.production)
        points = fmt(card.points, fg=0xFFA500)

        if card.points:
            return f"{i}: {c} → {p} + {points}"
        else:
            return f"{i}: {c} → {p}"

    @classmethod
    def coins_str(cls, coins):
        s = " ".join(
            fmt(f"{v}{COINS_LETTER[i]}", fg=i if v else 0x202020)
            for i, v in enumerate(coins)
        )
        return s

    @classmethod
    def player_str(cls, player):
        p = cls.coins_str(player.production)
        c = cls.coins_str(player.coins)
        if player.reserved:
            res = "\n".join(cls.card_str(c) for c in player.reserved)
            res = "\n" + fmt(res, indent="↳ ")
        else:
            res = "Nothing"
        pts = fmt(player.points, fg=0xFFA500)
        s = f"""
Production: {p}
Coins     : {c}
Points    : {pts}
Reserved  : {res}
""".strip()

        return s
