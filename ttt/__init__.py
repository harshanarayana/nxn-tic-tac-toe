from typing import List

from ttt.board import GameBoard, Move
from ttt.helper_util import AllMovesExhausedWithNoWinner
from ttt.player import Player


def create_player(name: str, symbol: str) -> Player:
    return Player(name=name, marker=symbol)


def create_board(size: int, p1: Player, p2: Player) -> GameBoard:
    return GameBoard(n=size, player1=p1, player2=p2)


def move_and_check_if_over(game: GameBoard, player: Player,
                           move: Move) -> Player:
    success = game.my_move(player=player, move=move)
    if success:
        for directions in [([0, 0], [-1, 1]), ([-1, 1], [0, 0]),
                           ([-1, 1], [-1, 1]), ([-1, 1], [1, -1])]:
            if _check_winner(game=game, player=player, move=move,
                             row_dirs=directions[0], col_dirs=directions[1]):
                return player

    elif game.exhausted_moves:
        raise AllMovesExhausedWithNoWinner()

    return None

def _check_board_and_score(game: GameBoard, player: Player, move: Move,
                           dir: List[int]) -> int:
    grid = game.cell(move=move)
    match = 0
    for i in range(1, game.win_count):
        row = grid.row + dir[0] * i
        col = grid.col + dir[1] * i
        if row < 0 or col < 0:
            break
        if row >= game.rows or col >= game.columns:
            break
        if game.get_grid(row=row, col=col).symbol != player.marker:
            break
        match += 1
    return match


def _check_winner(game: GameBoard, player: Player, move: Move,
                  row_dirs: List[int], col_dirs: List[int]) -> bool:
    if game.cell(move=move).symbol not in ["O", "X"]:
        return False
    score = 1
    for row_dir, col_dir in zip(row_dirs, col_dirs):
        score += _check_board_and_score(game=game, player=player, move=move,
                                        dir=[row_dir, col_dir])
        if score >= game.win_count:
            return True
    return False
