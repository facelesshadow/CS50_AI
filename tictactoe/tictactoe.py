"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for row in board:
        for element in row:
            if element == X:
                count += 1
    
    if count%2 == 0:
        return O
    else:
        return X




def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    i,j = 0
    moves = Set()
    for row in board:
        for element in row:
            if element == EMPTY:
                moves.add((i, j))
            j += 1
        i += 1

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.

    A copy of board
    current_player = player(board)
    on copy, at i, j, if element == EMPTY:
        copy[i,j] = current_player
        return copy
    else:
        raise Exception
    """

    duplicate = copy.deepcopy(board)
    current_player = player(board)

    if duplicate[action[0]][action[1]] == EMPTY:
        duplicate[action[0]][action[1]] = current_player
        return duplicate
    else:
        raise ValueError
    


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win = [
        [(0,0), (0,1), (0,2)], 
        [(1,0), (1,1), (1,2)], 
        [(2,0), (2,1), (2,2)], 
        [(0,0), (1,0), (2,0)], 
        [(0,1), (1,1), (2,1)], 
        [(0,2), (1,2), (2,2)],
        [(0,0), (1,1), (2,2)],
        [(0,2), (1,1), (2,0)]
        ]
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
