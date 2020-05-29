from collections import namedtuple

RED = 0
GREEN = 1
BLUE = 2
BLACK = 3
WHITE = 4
YELLOW = 5

COINS = {RED, GREEN, BLUE, BLACK, WHITE, YELLOW}
COINS_TO_NAMES = {
    RED: "red",
    GREEN: "green",
    BLUE: "blue",
    BLACK: "black",
    WHITE: "white",
    YELLOW: "yellow",
}

COINS_TO_JEWELL = {
    RED: "ruby",
    GREEN: "emerald",
    BLUE: "sapphire",
    BLACK: "onyx",
    WHITE: "diamond",
    YELLOW: "gold",
}

# Map from the color name / jewell name or number
NAME_TO_COINS = {color: i for i, color in COINS_TO_NAMES.items()}
NAME_TO_COINS.update({jewell: i for i, jewell in COINS_TO_JEWELL.items()})
NAME_TO_COINS.update({str(i): i for i in COINS_TO_NAMES})


STAGE = 6
PRODUCTION = 7
VICTORY_POINTS = 8
ID = 9

POINTS_FOR_WIN = 15
MIN_COINS_FOR_TAKE_TWO_SAME = 4
MAX_COINS_PER_PLAYER = 10
VISIBLE_CARDS = 4
MAX_RESERVED = 3
POINTS_PER_NOBLE = 3

START_YELLOW = 5
START_COINS = {
    2: 4,
    3: 5,
    4: 7,
}

Card = namedtuple(
    "Card",
    ("red", "green", "blue", "black", "white", "stage", "production", "points", "id"),
)

CARDS = (
    # ("Red", "Green", "Blue", "Black", "White", "Stage", "Production", "VP", "ID"),
    Card(0, 0, 3, 0, 0, "I", WHITE, 0, 0),
    Card(2, 0, 0, 1, 0, "I", WHITE, 0, 1),
    Card(1, 1, 1, 1, 0, "I", WHITE, 0, 2),
    Card(0, 0, 2, 2, 0, "I", WHITE, 0, 3),
    Card(0, 4, 0, 0, 0, "I", WHITE, 1, 4),
    Card(1, 2, 1, 1, 0, "I", WHITE, 0, 5),
    Card(0, 2, 2, 1, 0, "I", WHITE, 0, 6),
    Card(0, 0, 1, 1, 3, "I", WHITE, 0, 7),
    Card(0, 0, 0, 2, 1, "I", BLUE, 0, 8),
    Card(0, 0, 0, 3, 0, "I", BLUE, 0, 9),
    Card(1, 1, 0, 1, 1, "I", BLUE, 0, 10),
    Card(0, 2, 0, 2, 0, "I", BLUE, 0, 11),
    Card(4, 0, 0, 0, 0, "I", BLUE, 1, 12),
    Card(2, 1, 0, 1, 1, "I", BLUE, 0, 13),
    Card(2, 2, 0, 0, 1, "I", BLUE, 0, 14),
    Card(1, 3, 1, 0, 0, "I", BLUE, 0, 15),
    Card(0, 0, 1, 0, 2, "I", GREEN, 0, 16),
    Card(3, 0, 0, 0, 0, "I", GREEN, 0, 17),
    Card(1, 0, 1, 1, 1, "I", GREEN, 0, 18),
    Card(2, 0, 2, 0, 0, "I", GREEN, 0, 19),
    Card(0, 0, 0, 4, 0, "I", GREEN, 1, 20),
    Card(1, 0, 1, 2, 1, "I", GREEN, 0, 21),
    Card(2, 0, 1, 2, 0, "I", GREEN, 0, 22),
    Card(0, 1, 3, 0, 1, "I", GREEN, 0, 23),
    Card(0, 1, 2, 0, 0, "I", RED, 0, 24),
    Card(0, 0, 0, 0, 3, "I", RED, 0, 25),
    Card(0, 1, 1, 1, 1, "I", RED, 0, 26),
    Card(2, 0, 0, 0, 2, "I", RED, 0, 27),
    Card(0, 0, 0, 0, 4, "I", RED, 1, 28),
    Card(0, 1, 1, 1, 2, "I", RED, 0, 29),
    Card(0, 1, 0, 2, 2, "I", RED, 0, 30),
    Card(1, 0, 0, 3, 1, "I", RED, 0, 31),
    Card(1, 2, 0, 0, 0, "I", BLACK, 0, 32),
    Card(0, 3, 0, 0, 0, "I", BLACK, 0, 33),
    Card(1, 1, 1, 0, 1, "I", BLACK, 0, 34),
    Card(0, 2, 0, 0, 2, "I", BLACK, 0, 35),
    Card(0, 0, 4, 0, 0, "I", BLACK, 1, 36),
    Card(1, 1, 2, 0, 1, "I", BLACK, 0, 37),
    Card(1, 0, 2, 0, 2, "I", BLACK, 0, 38),
    Card(3, 1, 0, 1, 0, "I", BLACK, 0, 39),
    Card(5, 0, 0, 0, 0, "II", WHITE, 2, 40),
    Card(0, 0, 0, 0, 6, "II", WHITE, 3, 41),
    Card(2, 3, 0, 2, 0, "II", WHITE, 1, 42),
    Card(4, 1, 0, 2, 0, "II", WHITE, 2, 43),
    Card(3, 0, 3, 0, 2, "II", WHITE, 1, 44),
    Card(5, 0, 0, 3, 0, "II", WHITE, 2, 45),
    Card(0, 0, 5, 0, 0, "II", BLUE, 2, 46),
    Card(0, 0, 6, 0, 0, "II", BLUE, 3, 47),
    Card(3, 2, 2, 0, 0, "II", BLUE, 1, 48),
    Card(1, 0, 0, 4, 2, "II", BLUE, 2, 49),
    Card(0, 3, 2, 3, 0, "II", BLUE, 1, 50),
    Card(0, 0, 3, 0, 5, "II", BLUE, 2, 51),
    Card(0, 5, 0, 0, 0, "II", GREEN, 2, 52),
    Card(0, 6, 0, 0, 0, "II", GREEN, 3, 53),
    Card(0, 0, 3, 2, 2, "II", GREEN, 1, 54),
    Card(3, 2, 0, 0, 3, "II", GREEN, 1, 55),
    Card(0, 0, 2, 1, 4, "II", GREEN, 2, 56),
    Card(0, 3, 5, 0, 0, "II", GREEN, 2, 57),
    Card(0, 0, 0, 5, 0, "II", RED, 2, 58),
    Card(6, 0, 0, 0, 0, "II", RED, 3, 59),
    Card(2, 0, 0, 3, 2, "II", RED, 1, 60),
    Card(0, 2, 4, 0, 1, "II", RED, 2, 61),
    Card(2, 0, 3, 3, 0, "II", RED, 1, 62),
    Card(0, 0, 0, 5, 3, "II", RED, 2, 63),
    Card(0, 0, 0, 0, 5, "II", BLACK, 2, 64),
    Card(0, 0, 0, 6, 0, "II", BLACK, 3, 65),
    Card(0, 2, 2, 0, 3, "II", BLACK, 1, 66),
    Card(2, 4, 1, 0, 0, "II", BLACK, 2, 67),
    Card(0, 3, 0, 2, 3, "II", BLACK, 1, 68),
    Card(3, 5, 0, 0, 0, "II", BLACK, 2, 69),
    Card(0, 0, 0, 7, 0, "III", WHITE, 4, 70),
    Card(0, 0, 0, 7, 3, "III", WHITE, 5, 71),
    Card(3, 0, 0, 6, 3, "III", WHITE, 4, 72),
    Card(5, 3, 3, 3, 0, "III", WHITE, 3, 73),
    Card(0, 0, 0, 0, 7, "III", BLUE, 4, 74),
    Card(0, 0, 3, 0, 7, "III", BLUE, 5, 75),
    Card(0, 0, 3, 3, 6, "III", BLUE, 4, 76),
    Card(3, 3, 0, 5, 3, "III", BLUE, 3, 77),
    Card(0, 0, 7, 0, 0, "III", GREEN, 4, 78),
    Card(0, 3, 7, 0, 0, "III", GREEN, 5, 79),
    Card(0, 3, 6, 0, 3, "III", GREEN, 4, 80),
    Card(3, 0, 3, 3, 5, "III", GREEN, 3, 81),
    Card(0, 7, 0, 0, 0, "III", RED, 4, 82),
    Card(3, 7, 0, 0, 0, "III", RED, 5, 83),
    Card(3, 6, 3, 0, 0, "III", RED, 4, 84),
    Card(0, 3, 5, 3, 3, "III", RED, 3, 85),
    Card(7, 0, 0, 0, 0, "III", BLACK, 4, 86),
    Card(7, 0, 0, 3, 0, "III", BLACK, 5, 87),
    Card(6, 3, 0, 3, 0, "III", BLACK, 4, 88),
    Card(3, 5, 3, 0, 3, "III", BLACK, 3, 89),
)

STAGES = ("I", "II", "III")


NOBLES = (
    # r, e, s, o, d, y
    # (Red, green, blue, black, white, yellow)
    (3, 3, 0, 3, 0, 0),
    # "3r 3g 3k",
    (0, 0, 3, 3, 3, 0),
    # 'ooodddsss',
    (0, 3, 3, 0, 3, 0),
    # 'dddssseee',
    (3, 3, 3, 0, 0, 0),
    # 'sssrrreee',
    (3, 0, 3, 3, 0, 0),
    # 'ooorrreee',
    (3, 0, 0, 3, 3, 0),
    # 'ooorrrddd',
    (4, 4, 0, 0, 0, 0),
    # "4r 4g",
    (0, 0, 4, 0, 4, 0),
    # 'ssssdddd',
    (0, 4, 4, 0, 0, 0),
    # 'sssseeee',
    (4, 0, 0, 4, 0, 0),
    # 'oooorrrr',
)
