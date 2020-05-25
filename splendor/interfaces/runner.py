from itertools import cycle

from splendor.game import Game, PublicState, TakeAction
from splendor.game.errors import SplendorException


__all__ = ["BaseViewClient", "BaseClient", "Runner"]


class BaseViewClient:
    """Base class for splendor renderers."""

    def show(self, game: Game):
        """Called at the start of every turn to show the board."""

    def show_error(self, error: SplendorException):
        """Called when an exception occurs."""


class BaseClient:
    """Base class for all AIs, Player inputs etc...."""

    def play(self, state: PublicState):
        return TakeAction()

    def error(self, error: SplendorException):
        pass


class Runner:
    def __init__(self, *clients, view_client=None):
        self.view_client = view_client or BaseViewClient()
        self.clients = clients or [BaseClient() for _ in range(2)]
        self.game = Game(len(self.clients))

    def run(self):
        for i, client in cycle(enumerate(self.clients)):
            self.view_client.show(self.game)

            while True:
                # Resilient to bad actions
                try:
                    self.game.play(client.play(self.game.public_state))
                except SplendorException as e:
                    client.error(e)
                    self.view_client.show_error(e)
                else:
                    break

            if self.game.ended():
                break

        self.view_client.show(self.game)


if __name__ == "__main__":
    from splendor.interfaces.tui import TuiClient

    Runner(TuiClient("Félix"), TuiClient("Diego")).run()
