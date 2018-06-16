import sys
from typing import Dict

from ttt import *
from ttt.helper_util import PositionOccupiedException, InvalidCellPosition, \
    BgColors

players: Dict[int, Player] = {}

symbols = {
    1: "X",
    2: "O"
}


def get_color(current_player: Player):
    if current_player.marker.lower() == 'x':
        return BgColors.PURPLE
    else:
        return BgColors.ORANGE


def get_player_info(count: int) -> Player:
    while True:
        name = str(input("\nEnter name for Player {}: \n>> ".format(count)))
        if len(name) > 0:
            return Player(name=name, marker="{}".format(symbols[count]))


def get_move(current_player: Player) -> Move:
    while True:
        position = input(
            get_color(current_player=current_player) +
            "{}, choose a box to place an '{}' into: \n >> ".format(
                current_player.name,
                current_player.marker) + BgColors.RESET)
        if len(position) > 0:
            try:
                return Move(position=int(position))
            except ValueError:
                pass


def start_game(current_game: GameBoard):
    while True:
        turn = 0
        done = False
        while turn <= current_game.max_moves and not done:
            whose_turn = (turn + 1) % 2 + 1
            while True:
                print("\n")
                print(current_game)
                move = get_move(players[whose_turn])
                try:
                    winner = move_and_check_if_over(game=current_game,
                                                    current_player=players[whose_turn],
                                                    move=move)
                    if winner is not None:
                        print("\n")
                        print(current_game)
                        print("Congratulations {} You have won.\n\n".format(
                            players[whose_turn].name))
                        done = True
                        break
                    else:
                        break
                except AllMovesExhausedWithNoWinner:
                    print("The Game has ended in a Tie. !!!")
                    done = True
                    break
                except PositionOccupiedException:
                    print(
                        "Position has already been taken. Please pick another.")
                except InvalidCellPosition:
                    print("You've picked an Invalid Cell. Please pick another.")
            turn += 1
            if turn == current_game.max_moves:
                print("The Game has ended in a Tie. !!!")
                break
        c = input(
            "You've successfully completed a game of Tic-Tac-Toe. "
            "Do you want to continue? [y/N]: ")
        if len(c) < 1:
            sys.exit(0)
        elif len(c) > 1:
            sys.exit(0)
        elif c.upper() == 'Y':
            current_game.reset()
        else:
            sys.exit(0)


if __name__ == "__main__":
    while True:
        print("Welcome to a Game of Tic-Tac-Toe.\n\n")
        default_size = 3
        size = input(
            "Please Enter the Size of Board you want to Play with "
            "(NxN)[{}]: ".format(default_size))
        if len(size) < 1:
            size = 3
        else:
            try:
                size = int(size)
                if size < 0:
                    raise ValueError()
            except ValueError:
                print("You entered an Invalid Value. Defaulting to {}".format(
                    default_size))
                size = default_size

        default_win_count = size

        win_count = input(
            "Please Enter the Number of Marker in a Row that declares the "
            "player a winner [{}]: ".format(default_win_count))
        if len(win_count) < 1:
            win_count = 3
        else:
            try:
                win_count = int(win_count)
                if win_count > size or win_count < 0:
                    raise ValueError()
            except ValueError:
                print("You entered an Invalid Value. Defaulting to {}".format(
                    default_win_count))
                win_count = default_win_count

        player1 = get_player_info(1)
        player2 = get_player_info(2)
        players[1] = player1
        players[2] = player2
        game = GameBoard(n=size, win_count=win_count, player1=player1,
                         player2=player2)

        start_game(current_game=game)
