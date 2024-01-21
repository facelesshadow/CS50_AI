from tictactoe import minimax

X = "X"
O = "O"
EMPTY = None

board = [[X, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]]
answer = minimax(board)

print(f"answer is {answer}")