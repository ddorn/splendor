from copy import deepcopy
from random import shuffle

from splendor import *


def test_generate_diff_coins():
    ai = MinMaxAi()

    assert list(ai.generate_diff_coins(Coins(1, 0, 0, 1, 1, 1))) == [
        (0, ),
        (0, 3),
        (0, 3, 4),
        (0, 4),
        (3, ),
        (3, 4),
        (4, ),
    ]

    assert list(ai.generate_diff_coins(Coins(0, 2, 1, 1, 1, 1))) == [
        (1,),
        (1, 2),
        (1, 2, 3),
        (1, 2, 4),
        (1, 3),
        (1, 3, 4),
        (1, 4),
        (2,),
        (2, 3),
        (2, 3, 4),
        (2, 4),
        (3,),
        (3, 4),
        (4,),
    ]


def test_legal_moves():
    ai = MinMaxAi()
    game = Game(2)
    ps = game.public_state

    def explore(game, depth):
        if depth <= 0:
            return
        actions = list(ai.legal_moves(game.public_state))
        shuffle(actions)
        for action in actions[:3]:
            g = deepcopy(game)
            g.play(action)

            explore(g, depth - 1)

    explore(game, 6)

def test_legal_moves_linear():
    ai = MinMaxAi()
    game = Game(2)
    for i in range(40):
        actions = list(ai.legal_moves(game.public_state))
        shuffle(actions)
        game.play(actions[0])
