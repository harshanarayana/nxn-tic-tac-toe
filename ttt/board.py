from typing import List, Dict
from texttable import Texttable

from ttt.player import Player
from ttt.helper_util import (PositionOccupiedException,
                             InvalidCellPosition, AllMovesExhausedWithNoWinner,
                             BgColors)


class Move(object):
    """
    Class used to identify a move being selected by the User. This move
    represents a Cell Number on the NxN grid that is displayed on the user
    Screen.

    The numbers allowed to use range from 1 to NxN
    """

    def __init__(self, position: int):
        """
        Create a new Move Object.
        :param position: Cell Number selected by Player
        """
        self._position = position

    @property
    def position(self):
        """Get Selected Position by a Player"""
        return self._position

    def __str__(self):
        """String representation of a Move"""
        return "[Selected position: {]]".format(self._position)


class Grid(object):
    """
    This class is used to represent a Position on the Board with a specific
    value tagged to the Position.

    by default, the position value is a number representing the cell number
    that is tagged to the grid.

    However, when the Player makes a move, the value is updated from that
    number to the Marker that identifies the given user.
    """

    def __init__(self, row: int, col: int, symbol: str):
        """
        Create a Cell/Grid on the Game Board.

        :param row: Row Index for the Current Grid
        :param col: Column Index for the current Grid
        :param symbol: Symbol representing the Grid/Cell number
        """
        self._row: int = row
        self._col: int = col
        self._symbol: str = symbol

    @property
    def symbol(self):
        """Cell Data Identifier/Player Identification Marker"""
        return self._symbol

    @property
    def row(self):
        """Row Index representing the Grid on the Board"""
        return self._row

    @property
    def col(self):
        """Column Index representing the grid on the board"""
        return self._col

    @symbol.setter
    def symbol(self, value: str):
        """Set a Player Marker Identification if the move is valid"""
        self._symbol = value

    def __repr__(self):
        """String representation of the Grid Value"""
        return "[row: {} col: {} marker: {}]".format(self._row, self._col,
                                                     self._symbol)

    def __str__(self):
        """String representation of the Grid Value"""
        return "[row: {} col: {} marker: {}]".format(self._row, self._col,
                                                     self._symbol)


class GameBoard(object):
    """
    This class represents the NxN Board that will be used to play the Game.

    Based on the User Input, we use the default value or the value they have
    specified as the input data for generating the grid.
    """

    def __init__(self, player1: Player, player2: Player, n: int = 3,
                 win_count: int = 3):
        """
        Create a new Game Board to initiate a User Play.

        :param player1: Details of the Player 1
        :param player2: Details of the Player 2
        :param n: Size of the Game board. NxN size.
        :param win_count: Number of Markers in a row that tells you the winner.
        """
        self._rows: int = n
        self._columns: int = n
        self._win_count: int = win_count
        self._player1: Player = player1
        self._player2: Player = player2
        self._max_turn: int = self._rows * self._columns
        self._data: List[List[int]] = []
        self._grid_map: Dict[str, Grid] = {}
        self._index_to_grid_map: Dict[int, str] = {}
        self._moves_made: int = 0
        self._initialize_board()

    def _initialize_board(self):
        """Generate a Clean Game board and reset all the parameters"""
        self._moves_made = 0
        for row in range(0, self._rows):
            self._data.append([1] * self._columns)

        placeholder: List[List[str]] = []
        counter = 1
        for row in range(0, self._rows):
            placeholder.append([])
            for col in range(0, self._columns):
                self._index_to_grid_map[counter] = self._get_key(row, col)
                placeholder[row].append(str(counter))
                counter += 1

        self._grid_map = {
            str(row) + "-" + str(col): Grid(row=row, col=col,
                                            symbol=placeholder[row][col])
            for row in range(0, self._rows) for col in range(0, self._columns)
        }

    @property
    def exhausted_moves(self):
        """Check if maximum allowed moves have been exhausted."""
        return self._moves_made == self._max_turn

    @property
    def rows(self):
        """Get number of Rows in the Game Board"""
        return self._rows

    @property
    def columns(self):
        """Get number of columns in the game board"""
        return self._columns

    @property
    def win_count(self):
        """Get the Number of Marker in a line that makes you the winner"""
        return self._win_count

    @property
    def max_moves(self):
        """Get Maximum number of moves that you are allowed to make."""
        return self._max_turn

    def get_grid(self, row: int, col: int) -> Grid:
        """Find the Grid corresponding to a Row and Column"""
        return self._grid_map[self._get_key(row, col)]

    def cell(self, move: Move) -> Grid:
        """Given a move, find the Grid corresponding to the move."""
        return self._grid_map[self._index_to_grid_map[move.position]]

    def _get_key(self, row: int, col: int):
        """Generate a Key item that will be used as a reverse lookup for grid"""
        return str(row) + "-" + str(col)

    def _find_who_occupied_the_cell(self, grid: Grid) -> Player:
        """Identify who is occupying the cell to which the move is being made"""
        return self._player1 if grid.symbol == self._player1.marker else self._player2

    def _color_me(self, symbol: str):
        space = "  "
        if len(symbol) < 2:
            space += " "

        if symbol.lower() == 'o':
            return BgColors.ORANGE + symbol + space + BgColors.RESET
        elif symbol.lower() == 'x':
            return BgColors.PURPLE + symbol + space + BgColors.RESET
        else:
            return BgColors.CYAN + symbol + space + BgColors.RESET

    def my_move(self, player: Player, move: Move) -> bool:
        """
        Do careful checks and balance and perform a move.

        1. Check if I've already exhausted the max number of moves.
        2. Check if the Position of movement is valid.
        3. Check if the position is already occupied by someone.
        """
        if self._moves_made == self._max_turn:
            raise AllMovesExhausedWithNoWinner()
        if move.position in self._index_to_grid_map and player is not None:
            key = self._index_to_grid_map[move.position]
            if (self._grid_map[key].symbol not in [self._player1.marker,
                                                   self._player2.marker]):
                self._grid_map[key].symbol = player.marker
                self._moves_made += 1
                return True
            else:
                raise PositionOccupiedException(
                    "Cell already Occupied by: {}".format(
                        self._find_who_occupied_the_cell(
                            self._grid_map[key]).name))
        else:
            raise InvalidCellPosition(
                "Selected Position: {} is invalid".format(move.position))

    def reset(self):
        """Reset the board to clean state. Restart the game?"""
        self._initialize_board()

    def __str__(self):
        string = '-------' * self.rows + '--' * (self.columns - 1)
        string += "\n"
        for row in [
            [self._color_me(self._grid_map[self._get_key(row, col)].symbol) for
             col in range(0, self._columns)] for row in range(0, self._rows)]:
            string += "  |  ".join([i for i in row])
            string += "\n"
            string += '-------' * self.rows + '--' * (self.columns - 1)
            string += "\n"
        return string
