from splendor import Game, BaseGame, TakeAction
from splendor.game.errors import SplendorException


class BaseViewClient:
    """Base class for splendor renderers."""

    def show(self, game: Game):
        """Called at the start of every turn to show the board."""

    def show_error(self, error: SplendorException):
        """Called when an exception occurs."""


class BaseClient:
    """Base class for all AIs, Player inputs etc...."""

    def play(self, state: BaseGame):
        return TakeAction()

    def error(self, error: SplendorException):
        pass