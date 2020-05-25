import re

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion, NestedCompleter
from prompt_toolkit.contrib.regular_languages import compile
from prompt_toolkit.contrib.regular_languages.lexer import GrammarLexer
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.validation import ValidationError, Validator

from data import *
from game import *
from game.errors import ActionParseError
from splendor.runner import BaseClient


from prompt_toolkit.lexers import Lexer
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles.named_colors import NAMED_COLORS


class ActionLexer(Lexer):
    def lex_document(self, document):
        colors = list(sorted(NAMED_COLORS, key=NAMED_COLORS.get))

        # Colors can be named
        rev = {color: i for i, color in COINS_TO_NAMES.items()}
        # Or digits
        rev.update({str(i): i for i in range(YELLOW + 1)})

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

            for w in words[1:]:
                if w.upper() in ["TAKE", "BUY", "RESERVE"]:
                    lex.append(("#ffffff", w))
                elif w.lower() in rev:
                    color = {
                        RED: "#FF0000",
                        GREEN: "#00FF00",
                        BLUE: "#0000FF",
                        BLACK: "#C06060",
                        WHITE: "#FFFFFF",
                        YELLOW: "#FFFF00",
                    }.get(rev[w.lower()])
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


class TuiClient(BaseClient):
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
            lexer=ActionLexer(),
        )

        action = Action.from_str(text)
        return action
