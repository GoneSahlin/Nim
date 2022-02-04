from nim_player import NimPlayer
import utils
import LukeMartin.nim_player
import CalebBarker.nim_player
# import EricGustin.nim_player
# import NateKirsch.NimPlayer


class Nim:
    """Represents a game board
    """

    def __init__(self):
        """Constructor
        """
        self.state = [1, 3, 5, 7, 9]  # the state of the board

        # create players
        self.players = []
        # self.players.append(NateKirsch.NimPlayer.NimPlayer())
        # self.players.append(EricGustin.nim_player.NimPlayer())
        # self.players.append(NimPlayer())

        self.players.append(NimPlayer())
        self.players.append(LukeMartin.nim_player.NimPlayer())
        self.players.append(CalebBarker.nim_player.NimPlayer())
        # for i in range(3):
        #     self.players.append(NimPlayer())

        self.cur_player = 0  # which player's turn it is

        self.loser = None

        self.history = []

    def print(self):
        """Prints out the board state
        """
        print('Current State:')
        for i in range(len(self.state)):
            print('Row ', i, ':', sep='', end='')
            for j in range(self.state[i]):
                print('|', end='')
            print()
        print()

    def make_move(self):
        """Makes the next move in the game
        """
        # get next move from the next player
        move = self.players[self.cur_player].play(self.state, self.history)

        # get the next state based on the move
        new_state = []
        for i in range(len(self.state)):
            new_state.append(self.state[i] + move[i])
        self.state = new_state

        self.history.append(self.state)

        self.cur_player = (self.cur_player + 1) % len(self.players)  # update cur_player to the next player

    def run(self):
        """Runs the game
        """
        game_over = False
        while not game_over:
            print('Player ', self.cur_player, 's Turn:', sep='')
            self.print()
            self.make_move()
            game_over = utils.check_game_over(self.state)

        self.loser = self.cur_player - 1
        print('Player', (self.cur_player - 1) % 3, 'loses!')
