from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion, NestedCompleter
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.validation import ValidationError, Validator

from data import *
from game import *
from game.errors import ActionParseError
from splendor.runner import BaseClient


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
        )

        action = Action.from_str(text)
        return action
