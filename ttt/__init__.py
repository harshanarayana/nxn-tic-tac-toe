from typing import List

from ttt.board import GameBoard, Move
from ttt.helper_util import AllMovesExhaustedWithNoWinner
from ttt.player import Player


def move_and_check_if_over(game: GameBoard, current_player: Player,
                           move: Move) -> Player:
    """
    This method is invoked from the main Game Runner utility to perform
    a move selected by the Current player and check if this move opted by
    the user gave him a winning board.

    In order to do this, we perform the move first and then do check for the
    following items

    1. Vertically from 0th Row and go down until row - d where d is the number
    of consecutive patterns required for winning. This will take care of the
    bottom edge.
    2. Horizontally from 0th Column to Col - d where d is the number of
    consecutive patterns required for winning.
    3. Diagonally from top to Bottom. Start and find all possible diagonal with
    minimum of d from the current position and lookup to see if the user has
    won. (left top to right bottom)
    4. Diagonally from bottom up (left bottom to right top)

    :param game: Game Board before the move is performed
    :param current_player: Player performing the current move
    :param move: Move opted by the Player
    :return: Return the Player if he/she has won the game. None otherwise
    """
    success = game.my_move(player=current_player, move=move)
    if success:
        for directions in [([0, 0], [-1, 1]), ([-1, 1], [0, 0]),
                           ([-1, 1], [-1, 1]), ([-1, 1], [1, -1])]:
            if _check_winner(game=game, current_player=current_player,
                             move=move,
                             row_dirs=directions[0], col_dirs=directions[1]):
                return current_player

    elif game.exhausted_moves:
        raise AllMovesExhaustedWithNoWinner()

    return None


def _check_board_and_score(game: GameBoard, current_player: Player, move: Move,
                           direction: List[int]) -> int:
    """
    Get the Player Score in the consecutive direction from the current move
    position.

    :param game: Game Board after the current move has been performed
    :param current_player: Player who performed the current valid move
    :param move: Move opted by the Player
    :param direction: Direction in which the Row and Columns are to be traversed
    :return: Number of consecutive patterns for the given user
    """
    grid = game.cell(move=move)
    match = 0
    for i in range(1, game.win_count):
        row = grid.row + direction[0] * i
        col = grid.col + direction[1] * i
        if row < 0 or col < 0:
            break
        if row >= game.rows or col >= game.columns:
            break
        if game.get_grid(row=row, col=col).symbol != current_player.marker:
            break
        match += 1
    return match


def _check_winner(game: GameBoard, current_player: Player, move: Move,
                  row_dirs: List[int], col_dirs: List[int]) -> bool:
    """
    Check and find if the Current move by the Player has yielded him a win.

    :param game: Game Board after the current move has been performed
    :param current_player: Player who performed the current valid move
    :param move: Move opted by the Player
    :param row_dirs: Directionality of the Row to traverse the grid
    :param col_dirs: Directionality of the Column to traverse the grid
    :return: True if the move has yielded a win False otherwise
    """
    if game.cell(move=move).symbol not in ["O", "X"]:
        return False
    score = 1
    for row_dir, col_dir in zip(row_dirs, col_dirs):
        score += _check_board_and_score(game=game,
                                        current_player=current_player,
                                        move=move,
                                        direction=[row_dir, col_dir])
        if score >= game.win_count:
            return True
    return False
