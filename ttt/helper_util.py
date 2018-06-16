class PositionOccupiedException(Exception):
    def __init__(self, message):
        super(PositionOccupiedException, self).__init__(message)


class InvalidCellPosition(Exception):
    def __init__(self, message):
        super(InvalidCellPosition, self).__init__(message)


class AllMovesExhaustedWithNoWinner(Exception):
    def __init__(self):
        super(AllMovesExhaustedWithNoWinner, self).__init__()


class BgColors(object):
    ORANGE = '\033[33m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WARNING = '\033[93m'
    RESET = '\033[0m'
