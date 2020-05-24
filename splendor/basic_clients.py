import random
import textwrap
from functools import partial
from pprint import pprint
from random import choice

from game import *
from data import *


_print = print

COINS_LETTER = "RGBKWY"


def _color(x: int):
    hexa = {
        RED: 0xFF0000,
        GREEN: 0x00FF00,
        BLUE: 0x0000FF,
        BLACK: 0xC06060,
        WHITE: 0xFFFFFF,
        YELLOW: 0xFFFF00,
    }.get(x, x)

    r = hexa >> 16 & 0xFF
    g = hexa >> 8 & 0xFF
    b = hexa & 0xFF

    return r, g, b


def ansi(*args):
    joined = ";".join(map(str, args))
    return f"\033[{joined}m"


def print(
    *args,
    fg=None,
    bg=None,
    bold=False,
    ul=False,
    reset=True,
    sep=" ",
    indent=0,
    ret=False,
    **kwargs,
):
    text = sep.join(map(str, args))

    if bold:
        # my bold is ugly
        # text = f"\033[1m{text}"
        fg = WHITE

    if fg is not None:
        text = ansi(38, 2, *_color(fg)) + text
    if bg is not None:
        text = ansi(38, 2, *_color(bg)) + text
    if ul:
        text = ansi(4) + text
    if reset:
        text += ansi()
    if indent:
        if isinstance(indent, int):
            indent = " " * indent
        text = textwrap.indent(text, indent)

    if ret:
        return text

    _print(text, **kwargs)


fmt = partial(print, ret=True)


class BasicViewClient:
    def show(self, game: Game):
        print(f" Player: {game.player_idx} ".center(32, "="))
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

    def card_str(self, card: Card):
        c = self.coins_str(Coins(*card[:YELLOW]))
        p = fmt(COINS_LETTER[card.production], fg=card.production)
        points = fmt(card.points, fg=0xFFA500)

        if card.points:
            return f"{c} → {p} + {points}"
        else:
            return f"{c} → {p}"

    def coins_str(self, coins):
        s = " ".join(
            fmt(f"{v}{COINS_LETTER[i]}", fg=i if v else 0x202020)
            for i, v in enumerate(coins)
        )
        return s

    def player_str(self, player):
        p = self.coins_str(player.production)
        c = self.coins_str(player.coins)
        if player.reserved:
            res = "\n".join(self.card_str(c) for c in player.reserved)
            res = "\n" + fmt(res, indent="↳ ")
        else:
            res = ""

        s = f"""
Production: {p}
Coins     : {c}
Points    : {player.points}
Reserved  : {res}
""".strip()

        return s


class BasicClient:
    name = "Basic"

    def play(self, public_state: PublicState):
        if random.random() < 0.7:
            return TakeAction(choice(list(range(YELLOW))))
        else:
            return ReserveAction("I")
