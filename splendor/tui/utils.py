import textwrap
from functools import partial

from data import *

__all__ = ["print", "fmt", "COINS_LETTER"]

_print = print

COINS_LETTER = "RGBKWY"


def _color(x: int):
    hexa = {
        RED: 0xFF0000,
        GREEN: 0x00FF00,
        BLUE: 0x0000FF,
        BLACK: 0xC06060,
        WHITE: 0xFFFFFF,
        YELLOW: 0xFFFF00,
    }.get(x, x)

    r = hexa >> 16 & 0xFF
    g = hexa >> 8 & 0xFF
    b = hexa & 0xFF

    return r, g, b


def ansi(*args):
    joined = ";".join(map(str, args))
    return f"\033[{joined}m"


def print(
    *args,
    fg=None,
    bg=None,
    bold=False,
    ul=False,
    it=False,
    reset=True,
    sep=" ",
    indent=0,
    ret=False,
    **kwargs,
):
    text = sep.join(map(str, args))

    if bold:
        # my bold is ugly
        # text = f"\033[1m{text}"
        fg = WHITE

    if fg is not None:
        text = ansi(38, 2, *_color(fg)) + text
    if bg is not None:
        text = ansi(38, 2, *_color(bg)) + text
    if ul:
        text = ansi(4) + text
    if it:
        text = ansi(3) + text
    if reset:
        text += ansi()
    if indent:
        if isinstance(indent, int):
            indent = " " * indent
        text = textwrap.indent(text, indent)

    if ret:
        return text

    _print(text, **kwargs)


fmt = partial(print, ret=True)
