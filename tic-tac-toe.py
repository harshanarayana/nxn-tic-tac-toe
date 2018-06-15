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


def get_color(player: Player):
    if player.marker.lower() == 'x':
        return BgColors.PURPLE
    else:
        return BgColors.ORANGE


def get_player_info(count: int) -> Player:
    while True:
        name = str(input("\nEnter name for Player {}: \n>> ".format(count)))
        if len(name) > 0:
            return Player(name=name, marker="{}".format(symbols[count]))


def get_move(player: Player) -> Move:
    while True:
        position = input(
            get_color(
                player=player) + "{}, choose a box to place an '{}' "
                                 "into: \n >> ".format(
                player.name,
                player.marker) + BgColors.RESET)
        if len(position) > 0:
            try:
                return Move(position=int(position))
            except ValueError:
                pass


def start_game(game: GameBoard):
    while True:
        turn = 0
        done = False
        while turn <= game.max_moves and not done:
            player = (turn + 1) % 2 + 1
            while True:
                print("\n")
                print(game)
                move = get_move(players[player])
                try:
                    winner = move_and_check_if_over(game=game,
                                                    player=players[player],
                                                    move=move)
                    if winner is not None:
                        print("\n")
                        print(game)
                        print("Congratulations {} You have won.\n\n".format(
                            players[player].name))
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
            if turn == game.max_moves:
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
            game.reset()
        else:
            sys.exit(0)


if __name__ == "__main__":
    while True:
        print("Welcome to a Game of Tic-Tac-Toe.\n\n")
        size = input(
            "Please Enter the Size of Board you want to Play with (NxN)[3]: ")
        if len(size) < 1:
            size = 3
        else:
            size = int(size)

        win_count = input(
            "Please Enter the Number of Marker in a Row that declares the "
            "player a winner [3]: ")
        if len(win_count) < 1:
            win_count = 3
        else:
            win_count = int(win_count)

        player1 = get_player_info(1)
        player2 = get_player_info(2)
        players[1] = player1
        players[2] = player2
        game = GameBoard(n=size, win_count=win_count, player1=player1,
                         player2=player2)

        start_game(game=game)
