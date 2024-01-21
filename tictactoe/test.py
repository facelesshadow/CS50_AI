from tictactoe import player

X = "X"
O = "O"
EMPTY = None

board = [[O, EMPTY, X], [X, O, O], [X, X, O]]

answer = player(board)

print(f"answer is {answer}")