
import random
import pickle

with open("q_table.pkl", "rb") as file:
    Q = pickle.load(file)

def check_result(board):
    winning_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in winning_lines:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if "" not in board:
        return "Draw"

    return None
