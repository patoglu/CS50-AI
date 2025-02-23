"""
Tic Tac Toe Player
"""

import math
import traceback


X = "X"
O = "O"
EMPTY = None


def is_all_filled(board):
    for row in board:
        for elem in row:
            if elem not in ['X', 'O']:
                return False
    return True


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    x_count = 0
    o_count = 0
    for row in board:
        for element in row:
            if element is X:
                x_count += 1
            if element is O:
                o_count += 1

    if x_count > o_count:
        return O
    if x_count == o_count:
        return X


def actions(board):

    possible_actions = set()
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] is EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if i < 0 or i > 2 or j < 0 or j > 2:
        raise OverflowError("Can't make that move.")
    elif board[i][j] is not EMPTY:
        raise ValueError("Can't make that move. Board is not empty")
    new_board = [row[:] for row in board]

    x_or_o = player(board)

    new_board[i][j] = x_or_o

    return new_board


def winner(board):
    def condition(first_elem, second_elem, third_elem, player):
        return first_elem == player and second_elem == player and third_elem == player

    num_rows = len(board)
    num_cols = len(board[0])

    for i in range(num_rows):
        if condition(board[i][0], board[i][1], board[i][2], 'O'):
            return O
        if condition(board[i][0], board[i][1], board[i][2], 'X'):
            return X

    for i in range(num_cols):
        if condition(board[0][i], board[1][i], board[2][i], 'O'):
            return O
        if condition(board[0][i], board[1][i], board[2][i], 'X'):
            return X

    if condition(board[0][0], board[1][1], board[2][2], 'O'):
        return O
    if condition(board[0][0], board[1][1], board[2][2], 'X'):
        return X

    if condition(board[2][0], board[1][1], board[0][2], 'O'):
        return O
    if condition(board[2][0], board[1][1], board[0][2], 'X'):
        return X

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    game_result = winner(board)

    if is_all_filled(board) or game_result == O or game_result == X:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)

    if result is None:
        return 0
    elif result is X:
        return 1
    elif result is O:
        return -1


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)
    if current_player == 'X':
        _, move = max_value(board)
    else:
        _, move = min_value(board)

    return move


def max_value(state):
    if terminal(state):
        return utility(state), None

    v = -float('inf')
    best_action = None
    for action in actions(state):
        min_val, _ = min_value(result(state, action))
        if min_val > v:
            v = min_val
            best_action = action

    return v, best_action


def min_value(state):
    if terminal(state):
        return utility(state), None

    v = float('inf')
    best_action = None
    for action in actions(state):
        max_val, _ = max_value(result(state, action))
        if max_val < v:
            v = max_val
            best_action = action

    return v, best_action
