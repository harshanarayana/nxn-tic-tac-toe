from typing import List

from ttt.board import GameBoard, Move
from ttt.helper_util import AllMovesExhaustedWithNoWinner
from ttt.player import Player


def move_and_check_if_over(game: GameBoard, current_player: Player,
                           move: Move) -> Player:
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
