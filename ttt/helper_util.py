class PositionOccupiedException(Exception):
    """Attempted to perform a move on the Grid cell with other user's marker"""
    def __init__(self, message):
        super(PositionOccupiedException, self).__init__(message)


class InvalidCellPosition(Exception):
    """Invalid Cell Number selected. Too high/low/invalid characters"""
    def __init__(self, message):
        super(InvalidCellPosition, self).__init__(message)


class AllMovesExhaustedWithNoWinner(Exception):
    """Current move performed by the user has finished all possible moves"""
    def __init__(self):
        super(AllMovesExhaustedWithNoWinner, self).__init__()


class BgColors(object):
    """Color Patterns for identify different players on the board"""
    ORANGE = '\033[33m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WARNING = '\033[93m'
    RESET = '\033[0m'
