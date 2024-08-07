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
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    return type - Set of tuples - {(i, j), (k, l)}
    """

    moves = set()
    i = 0
    while i < 3:
        j = 0
        while j < 3:
            if board[i][j] == EMPTY:
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
    wins = [
        [[0,0], [0,1], [0,2]], 
        [[1,0], [1,1], [1,2]], 
        [[2,0], [2,1], [2,2]], 
        [[0,0], [1,0], [2,0]], 
        [[0,1], [1,1], [2,1]], 
        [[0,2], [1,2], [2,2]],
        [[0,0], [1,1], [2,2]],
        [[0,2], [1,1], [2,0]]
        ]

    signs = [X, O]
    for player in signs:
        for element in wins:
            if board[element[0][0]][element[0][1]] == player and board[element[1][0]][element[1][1]] == player and board[element[2][0]][element[2][1]] == player:
                return player

    return None


def terminal(board):
    """
    Returns True if game is over, False if game is not over.
    """

    if winner(board) == None:
        for row in board:
            for element in row:
                if element == EMPTY:
                    return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    answer = winner(board)
    if answer == X:
        return 1
    elif answer == O:
        return -1
    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return utility(board)

    if player(board) == X:
        v = float('-inf')
        print(actions(board))
        for action in actions(board):
            v = max(v, minimax(result(board, action)))
            return v
    
    if player(board) == O:
        v = float('inf')
        print(actions(board))
        for action in actions(board):
            v = min(v, minimax(result(board, action)))
            return v

    if terminal(board):
        return None    

    
