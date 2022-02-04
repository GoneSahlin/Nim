from nim import Nim
import nim_player
import sys


def main():
    """Main
    """
    out = sys.stdout
    sys.stdout = open('output.txt', 'w')  # change output to output.txt

    losses = [0, 0, 0]

    for _ in range(1000):
        game = Nim()  # creates a game
        game.run()  # runs the game
        losses[game.loser] = losses[game.loser] + 1
        # nim_player.evaluate_players(game.history)

    sys.stdout = out
    print(losses)





main()
