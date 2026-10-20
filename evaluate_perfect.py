import random
import pickle
from functools import lru_cache

with open("q_table.pkl", "rb") as file:
    Q = pickle.load(file)

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def available_moves(board):
    return [i for i in range(9) if board[i] == ""]


def check_result(board):
    for a, b, c in LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if "" not in board:
        return "Draw"

    return None


# X maximizes its result; O minimizes it.
@lru_cache(maxsize=None)
def minimax(board_tuple, player):
    board = list(board_tuple)
    result = check_result(board)

    if result == "X":
        return 1
    if result == "O":
        return -1
    if result == "Draw":
        return 0

    scores = []

    for move in available_moves(board):
        board[move] = player
        next_player = "O" if player == "X" else "X"

        scores.append(minimax(tuple(board), next_player))
        board[move] = ""

    return max(scores) if player == "X" else min(scores)


def perfect_x_move(board):
    best_score = float("-inf")
    best_moves = []

    for move in available_moves(board):
        board[move] = "X"
        score = minimax(tuple(board), "O")
        board[move] = ""

        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    return random.choice(best_moves)


DEBUG_SHOWN = False


def ai_move(board):
    global DEBUG_SHOWN

    moves = available_moves(board)
    state = tuple(board)

    values = [
        Q.get((state, "O", move), 0.0)
        for move in moves
    ]

    # Inspect the position before O's third move.
    target_board = ["", "O", "X", "", "", "X", "", "X", "O"]

    if not DEBUG_SHOWN and board == target_board:
        print("\nQ-values before O's third move:")

        for move, value in zip(moves, values):
            print(f"Square {move + 1}: Q-value = {value:.4f}")

        DEBUG_SHOWN = True

    best = max(values)

    return random.choice([
        move
        for move, value in zip(moves, values)
        if value == best
    ])


def evaluate_perfect(games=1000):
    wins = losses = draws = 0

    for game_number in range(games):
        board = [""] * 9
        history = []

        while True:
            # Perfect opponent X moves first.
            move = perfect_x_move(board)
            board[move] = "X"
            history.append(("X", move + 1))

            result = check_result(board)
            if result is not None:
                break

            # Learned AI plays O.
            move = ai_move(board)
            board[move] = "O"
            history.append(("O", move + 1))

            result = check_result(board)
            if result is not None:
                break

        if result == "X":
            losses += 1
            print(f"\nLoss found in game {game_number + 1}")
            print("Final board:")

            for i in range(0, 9, 3):
                print(board[i:i + 3])

            print("Move sequence:", history)

        elif result == "O":
            wins += 1
        else:
            draws += 1

    print("\n--- Perfect Opponent Evaluation ---")
    print(f"Games:  {games}")
    print(f"Wins:   {wins} ({wins / games * 100:.1f}%)")
    print(f"Losses: {losses} ({losses / games * 100:.1f}%)")
    print(f"Draws:  {draws} ({draws / games * 100:.1f}%)")


if __name__ == "__main__":
    evaluate_perfect(1000)