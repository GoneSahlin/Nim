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
    for i in range(len(state)):  # loop through values in state
        for j in range(1, state[i] + 1):  # loop i times, starting at 1, ending at i + 1
            move_list.append((i, j))  # appends the possible move to move_list

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
