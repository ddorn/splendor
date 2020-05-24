class SplendorException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.msg}"


class TakeCoinsException(SplendorException):
    def __init__(self, msg, action):
        self.action = action
        super(TakeCoinsException, self).__init__(msg)

    def __repr__(self):
        return f"{super().__repr__()} - {self.action}"


class NotEnoughCoins(SplendorException):
    def __init__(self, available, wanted):
        self.available = available
        self.wanted = wanted
        super().__init__(f"Wanted {self.wanted} when there is only {self.available}.")
