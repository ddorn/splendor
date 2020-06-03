from prompt_toolkit import Application

from splendor import Game
from splendor.game.errors import SplendorException
from splendor.interfaces.base import BaseViewClient


class TuiView(BaseViewClient):
    def __init__(self):
        self.app = Application()
