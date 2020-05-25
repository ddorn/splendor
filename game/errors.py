from data import MAX_COINS_PER_PLAYER, MAX_RESERVED


class SplendorException(Exception):
    def __init__(self, msg, *args, **kwargs):
        self.msg = msg
        self.args = args
        self.kwargs = kwargs

        for name, value in kwargs.items():
            setattr(self, name, value)

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.msg} | {self.args} || {self.kwargs}"

    def __str__(self):
        return repr(self)


class TakeCoinsException(SplendorException):
    action: "TakeAction"

    def __init__(self, msg, action):
        super(TakeCoinsException, self).__init__(msg, action=action)


class NotEnoughCoins(SplendorException):
    wanted: "Coins"
    available: "Coins"

    def __init__(self, available, wanted):
        super().__init__(
            f"Wanted {wanted} when there is only {available}.",
            wanted=wanted,
            available=available,
        )


class TooManyCoins(SplendorException):
    taking: int
    total: int

    def __init__(self, taking, total):
        super().__init__(
            f"Trying to take more than {MAX_COINS_PER_PLAYER} coins.",
            taking=taking,
            total=total,
        )


class EmptyDeck(SplendorException):
    stage: str

    def __init__(self, stage):
        super().__init__(f"No more cards in stage {stage}", stage=stage)


class NoSuchCard(SplendorException):
    card_id: int

    def __init__(self, card_id):
        super().__init__(f"No such card available: {card_id}", card_id=card_id)


class ReserveFull(SplendorException):
    def __init__(self):
        super().__init__(f"There are already {MAX_RESERVED} cards reserved.")


class ActionParseError(SplendorException):
    pass


class GameEnded(SplendorException):
    def __init__(self):
        super().__init__("The game is has ended.")
