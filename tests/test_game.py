from dataclasses import FrozenInstanceError

from pytest import raises

from data import *
from game import *
from game.errors import *


def test_game_init():
    game = Game(None, None)

    assert len(game.nobles) == 3

    for color in [RED, GREEN, BLUE, BLACK, WHITE]:
        assert game.bank[color] == START_COINS[2]
    assert game.bank[YELLOW] == START_YELLOW


def test_game_public_state_immutable():
    game = Game(None, None)
    state = game.public_state

    with raises(AttributeError):
        state.players[0].points += 1

    with raises(TypeError):
        state.players[0] = None

    with raises(AttributeError):
        state.coins[0].red += 1

    with raises(AttributeError):
        state.coins.white = 0

    with raises(TypeError):
        state.cards[0] = None

    with raises(AttributeError):
        state.coins = None

    with raises(TypeError):
        state.cards[0][0] = None

    with raises(TypeError):
        state.cards[0][0][0] = None


def test_game_public_state():
    game = Game(None, None)

    for age in game.public_state.cards:
        assert len(age) == 4


def test_game_take_action():
    game = Game(None, None)

    player = game.players[0]

    game.action(player, TakeAction(RED))
    with raises(NotEnoughCoins):
        game.action(player, TakeAction(RED, RED))

    for i in range(3):
        game.action(player, TakeAction(RED, GREEN, BLUE))

    assert player.coins == Coins(4, 3, 3)
    assert game.bank == Coins(0, 1, 1, 4, 4, 5)

    with raises(TakeCoinsException):
        game.action(player, TakeAction(YELLOW))

    with raises(TooManyCoins):
        game.action(player, TakeAction(BLUE))


def test_game_take_action2():
    game = Game(None, None)
    p1, p2 = game.players

    for i in range(2):
        for p in (p1, p2):
            game.action(p, TakeAction(BLUE))
            assert p.coins == Coins(blue=i + 1)

    with raises(NotEnoughCoins):
        game.action(p1, TakeAction(BLUE))
