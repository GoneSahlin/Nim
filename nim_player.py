import random
from queue import Queue


class NimPlayer:
    """Represents a player that can play Nim
    """

    def __init__(self):
        """Constructor
        """
        pass

    def play(self, state, history):
        """Makes a move by checking if each state created by each possible move is winning. It will pick the first move
        that is winning, and if none of moves are winning, then it will choose a random move.

        Parameters
        ----------
        state : the state of the board, a list of the number of lines in each row

        Returns
        -------
        move : the number removed from a row, e.g. [0,-2,0,0,0]
        """
        tree = Tree(state)
        tree.build_tree()

        tree.root.calculate_scores()
        print(tree.root.scores)

        # find child with best probability
        best_score = 0
        best_child = []
        for child in tree.root.children:
            if child.scores[2] > best_score:
                best_score = child.scores[2]
                best_child = [child]
            elif child.scores[2] == best_score:
                best_child.append(child)

        # pick a random child in best_child
        chosen_child = random.choice(best_child)

        # find the move corresponding to the child
        move_list = find_moves(state)
        for move in move_list:
            new_state = project_state(state, move)
            simplified_state = new_state.copy()
            simplified_state.sort()
            if chosen_child.state == simplified_state:
                reformatted_move = reformat_move(move, len(state))  # change move into format required
                return reformatted_move


class Tree:
    """A tree to be used to find the possible future states
    """

    class TreeNode:
        """A node on the tree
        """

        def __init__(self, state, parent):
            """Constructor
            """
            self.state = state
            self.parent = parent
            self.children = []
            self.scores = []  # a list of the probabilities of each player winning, starting with the player to go next

        def calculate_scores(self):
            """Calculates the probabilities of each player winning
            """
            if sum(self.state) == 0:
                self.scores = [1, 1, 0]
                return

            # calculate child scores
            for child in self.children:
                if not child.scores:
                    child.calculate_scores()

            # find best move
            best_score = 0
            best_child = []
            for child in self.children:
                if child.scores[2] > best_score:
                    best_score = child.scores[2]
                    best_child = [child]
                elif child.scores[2] == best_score:
                    best_child.append(child)

            # calculate nodes scores
            first_scores = []
            second_scores = []
            for child in best_child:
                first_scores.append(child.scores[0])
                second_scores.append(child.scores[1])

            self.scores = [best_score, sum(first_scores) / len(first_scores), sum(second_scores) / len(second_scores)]

    def __init__(self, state):
        """Constructor
        """
        self.root = self.__class__.TreeNode(state, None)

    def build_tree(self):
        """Builds the tree of possible future states
        """
        node_dict = {}

        q = Queue()
        q.put(self.root)

        while not q.empty():
            node = q.get()

            move_list = find_moves(node.state)

            for move in move_list:
                new_state = project_state(node.state, move)
                new_state.sort()
                string_state = str(new_state)

                # check if new node
                if string_state in node_dict:
                    child = node_dict[string_state]
                else:
                    child = self.__class__.TreeNode(new_state, node)
                    node_dict[string_state] = child
                    q.put(child)

                node.children.append(child)


def evaluate_players(history):
    """Evaluates how good each player is, or how much they lowered their probability of winning throughout the game

    Parameters
    ----------
    history : an list of all previous states

    Returns
    -------

    """
    starting_state = [1, 3, 5, 7, 9]
    tree = Tree(starting_state)
    tree.build_tree()
    tree.root.calculate_scores()

    # split history states by player
    # it is currently player 0's turn
    player_histories = [[], [], []]
    for i in range(len(history) - 1, -1, -1):  # loop through history backwards
        player_histories[(len(history) - i) % 3].append(history[i])

    print(player_histories)




def find_moves(state):
    """Finds all possible moves

    Parameters
    ----------
    state : the state of the board, a list of the number of lines in each row

    Returns
    -------
    move_list : a list of all possible moves, each move a tuple containing (row, number of lines to remove)
    """
    move_list = []  # list of possible moves
    for row in range(len(state)):  # loop through values in state
        for num_removed in range(1, 4):  # loop 3 times because you can only take 3 per turn
            if state[row] >= num_removed:  # move only possible if there are enough sticks in the row
                move_list.append((row, num_removed))  # appends the possible move to move_list

    return move_list


def project_state(state, move):
    """Projects a state after the move has been made

    Parameters
    ----------
    state : the state of the board, a list of the number of lines in each row
    move : instructions for a move, a tuple containing (row, number of lines to remove)

    Returns
    -------
    new_state : the state of the board after the move is made, a list of the number of lines in each row
    """
    new_state = state.copy()

    new_value = state[move[0]] - move[1]
    new_state[move[0]] = new_value

    return new_state


def check_game_over(state):
    """Checks if the game is over by checking if all the values in state are 0

    Returns
    -------
    game_over : if the game is over
    """
    game_over = True  # game is over if all values are 0
    for val in state:
        if val != 0:
            game_over = False  # returns False if any value in state is not 0

    return game_over


def reformat_move(move_in, num_rows):
    """Reformats the move to the required format

    Parameters
    ----------
    move_in : the move formatted as a tuple containing (row, number of lines to remove)
    num_rows : the number of rows in a state

    Returns
    -------
    move_out : the move formatted as a list containing the number of lines to remove from each row
    """
    move_out = []
    for i in range(num_rows):
        if i == move_in[0]:
            move_out.append(-move_in[1])
        else:
            move_out.append(0)

    return move_out
