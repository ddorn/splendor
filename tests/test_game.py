from copy import deepcopy

from pytest import raises

from splendor.data import *
from splendor.game import *
from splendor.game.coins import one_coins, yellow_coin
from splendor.game.errors import *


def test_game_init():
    game = Game(2)

    assert len(game.nobles) == 3

    for color in [RED, GREEN, BLUE, BLACK, WHITE]:
        assert game.bank[color] == START_COINS[2]
    assert game.bank[YELLOW] == START_YELLOW


def test_game_public_state_no_refs():
    game = Game(2)
    original_game = deepcopy(game)

    state = game.public_state

    state.players[0].points += 1
    state.players[1] = None
    with raises(TypeError):
        state.bank[0] += 1
    with raises(AttributeError):
        state.bank.white = 0
    state.deck[1] = None
    state.bank = None
    state.deck[0][0] = None

    with raises(TypeError):
        state.deck[0][0][0] = None

    assert original_game == game


def test_game_public_state():
    game = Game(2)

    ps = game.public_state

    assert len(ps.deck) == 3
    for age in ps.revealed_cards():
        assert len(age) == 4

    assert len(ps.nobles) == 3
    assert ps.bank == game.bank
    assert ps.current_player_id == game.current_player_id
    assert len(ps.players) == len(game.players)


def test_game_take_action():
    game = Game(2)

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
    game = Game(2)
    p1, p2 = game.players

    for i in range(2):
        for p in (p1, p2):
            game.action(p, TakeAction(BLUE))
            assert p.coins == Coins(blue=i + 1)

    with raises(NotEnoughCoins):
        game.action(p1, TakeAction(BLUE))


def test_game_reserve_action_hidden():
    game = Game(2)
    p = game.players[1]

    for i in range(3):
        card = game.deck[i][VISIBLE_CARDS]
        game.action(p, ReserveAction(STAGES[i]))

        assert p.coins == Coins(yellow=i + 1)
        assert game.bank.yellow == 5 - (i + 1)
        assert card in p.reserved
        assert len(p.reserved) == i + 1

    with raises(ReserveFull):
        game.action(p, ReserveAction("I"))


def test_game_reserve_action_coins():
    game = Game(3)
    p1, p2, p3 = game.players

    for i in range(3):
        game.action(p1, TakeAction(RED, GREEN, BLUE))
    game.action(p1, ReserveAction("I"))

    assert p1.coins == Coins(3, 3, 3, yellow=1)

    game.action(p1, ReserveAction("I"))
    assert p1.coins.yellow == 1
    assert game.bank.yellow == 4

    for i in range(3):
        game.action(p2, ReserveAction("I"))
    assert p2.coins.yellow == 3

    game.action(p3, ReserveAction("I"))
    assert game.bank.yellow == 0
    assert p3.coins.yellow == 1

    game.action(p3, ReserveAction("I"))
    assert game.bank.yellow == 0
    assert p3.coins.yellow == 1


def test_game_reserve_visible():
    game = Game(2)
    p = game.players[0]

    to_reserve = game.deck[0][2]
    game.action(p, ReserveAction(to_reserve.id))

    assert to_reserve not in game.deck[0]
    assert to_reserve in p.reserved

    with raises(NoSuchCard):
        game.action(p, ReserveAction(to_reserve.id))

    assert p.coins == Coins(yellow=1)
    assert game.bank.yellow == 4


def test_game_check_noble():
    game = Game(2)
    p = game.players[0]

    p.production = Coins(*game.nobles[0])

    assert game.check_nobles(p)
    p.production -= Coins(1, 1, 1, 1)
    assert not game.check_nobles(p)


def test_game_buy_action():
    game = Game(2)
    p = game.players[0]

    with raises(NoSuchCard):
        game.action(p, ReserveAction(game.deck[2][VISIBLE_CARDS].id))

    game.action(p, ReserveAction("I"))
    card: Card = p.reserved[0]
    print(p)

    p.coins = Coins(*card[:YELLOW]) - Coins(1, 1, 1, 1, 1)
    with raises(NotEnoughCoins):
        game.action(p, BuyAction(card.id))

    p.coins += Coins(1, 1, 1, 1, 1)
    game.action(p, BuyAction(card.id))

    assert p.points == card.points
    assert card not in p.reserved
    assert p.production != Coins()


def test_buy_with_yellow():
    game = Game(2)
    p = game.players[0]
    card = game.deck[0][0]
    p.coins = Coins(*card[:YELLOW])

    # Remove one coin
    for c in p.coins.as_iter():
        p.coins -= one_coins[c]
        break

    p.coins += yellow_coin

    game.play(BuyAction(card.id))

    assert p.production.total() > 0


def test_game_buy_visible():
    game = Game(2)
    p = game.players[0]
    card = game.deck[0][0]

    p.coins = Coins(*card[:YELLOW])
    game.action(p, BuyAction(card.id))

    assert p.points == card.points
    assert p.production != Coins()


def test_game_end_exception():
    g = Game(2)
    g.players[0].points += 100

    assert g.ended()
    with raises(GameEnded):
        g.play(TakeAction())
