import itertools
from itertools import chain

from prompt_toolkit import ANSI
from prompt_toolkit.completion import Completer, Completion, NestedCompleter
from prompt_toolkit.lexers import Lexer
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import ValidationError, Validator

from splendor.data import *
from splendor.game import *
from splendor.game.errors import ActionParseError, SplendorException
from splendor.interfaces.runner import BaseClient
from .utils import COINS_LETTER, fmt, print, COINS_TO_COLOR, BG_COLOR, NO_COIN_COLOR


class ActionLexer(Lexer):
    def lex_document(self, document):
        def split_words(s: str):
            cur = ""
            for l in s:
                if l.isspace() and cur.strip():
                    yield cur
                    cur = ""
                elif not l.isspace() and not cur.strip():
                    yield cur
                    cur = ""
                cur += l
            if cur:
                yield cur

        def get_line(lineno):
            text = document.lines[lineno]
            lex = []

            words = list(split_words(text))

            if words:
                lex.append(("fg:white", words[0]))
            else:
                lex.append(("", ""))

            for w in words[1:]:
                if w.upper() in ["TAKE", "BUY", "RESERVE"]:
                    lex.append(("#ffffff", w))
                elif w.lower() in NAME_TO_COINS:
                    color = COINS_TO_COLOR.get(NAME_TO_COINS[w.lower()])
                    lex.append((color, w))
                elif w.isnumeric():
                    lex.append(("fg:pink", w))
                else:
                    lex.append(("", w))

            return lex

        return get_line


class ColorCompleter(Completer):
    def __init__(self, coins):
        self.coins = coins

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor().lower()

        for coin, color in chain(COINS_TO_NAMES.items(), COINS_TO_JEWELL.items()):
            if self.coins[coin] and color.startswith(word):
                yield Completion(
                    color.upper(),
                    start_position=-len(word),
                    style=f"bg:{BG_COLOR} fg:{COINS_TO_COLOR[coin]}",
                    selected_style="fg:white bg:" + COINS_TO_COLOR[coin],
                )


class ActionValidator(Validator):
    def validate(self, document):
        text = document.text

        try:
            Action.from_str(text)
        except ActionParseError as e:
            raise ValidationError(message=e.msg)


class TuiClient(BaseClient):
    def __init__(self, name="Basic"):
        self.name = name
        self.last_was_error = False

    def play(self, public_state: BaseGame):

        if not self.last_was_error:
            self.show(public_state)

        completer = NestedCompleter.from_nested_dict(
            {"TAKE": ColorCompleter(public_state.bank), "BUY": None, "RESERVE": None,}
        )

        def bottom_bar():
            sep = ("", " ")
            p = public_state.players[public_state.current_player_id]
            return [
                sep,
                ("#ffa500 bg:black", " Splendor "),
                sep,
                ("", self.name),
                ("", " > (total) "),
                *ANSI(
                    self.coins_str(p.coins + p.production)
                    .replace("38", "48")
                    .replace("32;32;32", "80;80;80")
                ).__pt_formatted_text__(),
            ]

        style = Style.from_dict(
            {
                "bottom-toolbar": f"fg:{BG_COLOR} bg:#bbb",
                "completion-menu.completion": f"fg:#bbb bg:{BG_COLOR}",
            }
        )

        text = prompt(
            f"Player {public_state.current_player_id}: ",
            completer=completer,
            validator=ActionValidator(),
            color_depth=ColorDepth.TRUE_COLOR,
            lexer=ActionLexer(),
            bottom_toolbar=bottom_bar,
            style=style,
        )

        action = Action.from_str(text)

        self.last_was_error = False
        return action

    def show(self, game: BaseGame):
        print("\033[2J", end="")  # clear screen
        print(f" Player: {self.name} ".center(32, "="))
        print()

        print("Nobles", ul=True)
        for noble in game.nobles:
            print(self.noble_str(noble), indent=2)
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

        print(fmt("Bank:", ul=True), self.coins_str(game.bank))
        print()

    def error(self, error: SplendorException):
        self.last_was_error = True
        print(error.msg, fg=0xFF0000)

    @classmethod
    def card_str(cls, card: Card):
        i = fmt(f"{card.id:>2}", it=True)
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
            fmt(f"{v}{COINS_LETTER[i]}", fg=i if v else NO_COIN_COLOR)
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

    @classmethod
    def noble_str(cls, noble: Coins):
        return f"{cls.coins_str(noble)} → {POINTS_PER_NOBLE}"
