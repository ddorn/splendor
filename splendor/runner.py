from itertools import cycle

from game import Game
from splendor.basic_clients import BasicViewClient, BasicClient


class Runner:
    def __init__(self, *clients, view_client=None):
        self.view_client = view_client or BasicViewClient()
        self.clients = clients or [BasicClient() for _ in range(2)]
        self.game = Game(len(self.clients))

    def run(self):
        for i, client in cycle(enumerate(self.clients)):
            self.view_client.show(self.game)
            self.game.play(client.play(self.game.public_state))


if __name__ == "__main__":
    Runner().run()