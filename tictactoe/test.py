from tictactoe import player

X = "X"
O = "O"
EMPTY = None

board = [[X, O, X],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]]
answer = player(board)

print(f"answer is {answer}")