import random
import pickle

# Load your trained Q-table
with open("q_table.pkl", "rb") as file:
    Q = pickle.load(file)

def get_available_moves(board):
    return [i for i in range(9) if board[i] == ""]

def check_result(board):
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    for a, b, c in lines:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]

    if "" not in board:
        return "Draw"

    return None

def ai_move(board, player):
    available = get_available_moves(board)
    state = tuple(board)

    values = [
        Q.get((state, player, move), 0.0)
        for move in available
    ]

    best_value = max(values)
    best_moves = [
        move for move, value in zip(available, values)
        if value == best_value
    ]

    return random.choice(best_moves)

def evaluate(games=1000):
    wins = losses = draws = 0

    for _ in range(games):
        board = [""] * 9

        # Alternate who moves first
        ai_player = random.choice(["X", "O"])
        opponent = "O" if ai_player == "X" else "X"
        current_player = "X"

        while True:
            if current_player == ai_player:
                move = ai_move(board, ai_player)
            else:
                move = random.choice(get_available_moves(board))

            board[move] = current_player
            result = check_result(board)

            if result is not None:
                if result == "Draw":
                    draws += 1
                elif result == ai_player:
                    wins += 1
                else:
                    losses += 1
                break

            current_player = "O" if current_player == "X" else "X"

    print("\n--- Evaluation Results ---")
    print(f"Games: {games}")
    print(f"Wins:   {wins} ({wins / games * 100:.1f}%)")
    print(f"Losses: {losses} ({losses / games * 100:.1f}%)")
    print(f"Draws:  {draws} ({draws / games * 100:.1f}%)")

if __name__ == "__main__":
    evaluate(1000)
