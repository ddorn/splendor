from itertools import cycle

from splendor.game import Game
from splendor.game.errors import SplendorException
from splendor.interfaces.base import BaseViewClient, BaseClient
from splendor.interfaces.tui.utils import fmt


__all__ = ["Runner"]


class Runner:
    def __init__(self, *clients, view_client=None):
        self.view_client = view_client or BaseViewClient()
        self.clients = clients or [BaseClient() for _ in range(2)]
        self.game = Game(len(self.clients))

    def run(self):
        turn = -1
        for i, client in cycle(enumerate(self.clients)):
            turn += 1
            print("Turn", fmt(turn, bold=True))
            self.view_client.show(self.game)

            while True:
                # Resilient to bad actions
                try:
                    self.game.play(client.play(self.game.public_state))
                except SplendorException as e:
                    client.error(e)
                    self.view_client.show_error(e)
                except KeyboardInterrupt:
                    print("\033[31mAborted.\033[m")
                    quit(1)
                else:
                    break

            if self.game.ended():
                break

        self.view_client.show(self.game)


if __name__ == "__main__":
    from splendor.interfaces.tui import TuiClient
    from splendor.interfaces.ai import MinMaxAi

    Runner(TuiClient("Felix"), MinMaxAi(), ).run()
