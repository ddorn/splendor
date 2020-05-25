import random
import textwrap
from functools import partial
from pprint import pprint
from random import choice

from prompt_toolkit.output import ColorDepth
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion, NestedCompleter
from prompt_toolkit.validation import Validator, ValidationError

from game import *
from data import *
from game.errors import ActionParseError, SplendorException

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
    it=False,
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
    if it:
        text = ansi(3) + text
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

        s = f"""
Production: {p}
Coins     : {c}
Points    : {player.points}
Reserved  : {res}
""".strip()

        return s


class ColorCompleter(Completer):
    def __init__(self, coins):
        self.coins = coins

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor().lower()

        for coin, color in COINS_TO_NAMES.items():
            if self.coins[coin] and color.startswith(word):
                yield Completion(
                    color.upper(),
                    start_position=-len(word),
                    style="fg:" + color,
                    selected_style="fg:white bg:" + color,
                )


class ActionValidator(Validator):
    def validate(self, document):
        text = document.text

        try:
            Action.from_str(text)
        except ActionParseError as e:
            raise ValidationError(message=e.msg)


class BasicClient:
    name = "Basic"

    def play(self, public_state: PublicState):
        completer = NestedCompleter.from_nested_dict(
            {"TAKE": ColorCompleter(public_state.coins), "BUY": None, "RESERVE": None,}
        )

        text = prompt(
            f"Player {public_state.current_player}: ",
            completer=completer,
            validator=ActionValidator(),
            color_depth=ColorDepth.TRUE_COLOR,
        )

        action = Action.from_str(text)
        return action
